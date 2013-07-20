#!/usr/bin/python

import os
import random
import sys
import subprocess
import shutil
import itertools

seed = 42
random.seed(seed)

sample_script=os.path.join(os.path.split(os.path.abspath(__file__))[0], "sample_population.py")
sgvs = ["high", "intermediate", "clone"]
hist_contings = ["pred", "nopred"]

if len(sys.argv) != 4:
    print >>sys.stderr, "USAGE: evaluation_replicate_generation.py <phase2_dir> <evaluation_out_dir> <population_from_update>"
    sys.exit(1)

phase2_dir=sys.argv[1]
phase3_dir=sys.argv[2]
seed_spop_update = sys.argv[3]

pairwise_skel_dir = { "pred" : os.path.join(phase3_dir, "skel/pairwise_skel_pred"), "nopred" : os.path.join(phase3_dir, "skel/pairwise_skel_nopred")}
pairwise_eval_path_pattern = os.path.join(phase3_dir,"pairwise/treatment_{0}/{1}_{2}_{3}__vs__{4}_{5}_{6}")

phase2_spop_pattern = { "pred" : os.path.join(phase2_dir, "pred_replicates/{0}/sim_{1}/data/detail-{2}.spop"), 
                        "nopred" : os.path.join(phase2_dir, "nopred_replicates/{0}/sim_{1}/data/detail-{2}.spop") }

cnt = 0
for sgv in sgvs:
    for ht in hist_contings:
        for phase2_rep in range(1, 31):
            print "Preparing pairwise phase3 competitions for treatment %s %s" % (sgv, ht)
            for sgv_opp in sgvs:
                for ht_opp in hist_contings:
                    if sgv == sgv_opp and ht == ht_opp:
                        continue

                    for treatment in ["pred", "nopred"]:
                        rep_opp = random.randint(1, 30)

                        print "{0}_{1}_{2} --- VS --- {3}_{4}_{5}".format(sgv, ht, phase2_rep, sgv_opp, ht_opp, rep_opp)
                        cnt += 1


                        curr_p3_dir = pairwise_eval_path_pattern.format(treatment, sgv, ht, phase2_rep, sgv_opp, ht_opp, rep_opp)
                        parent = os.path.split(curr_p3_dir)[0]
                        
                        if os.path.exists(curr_p3_dir):
                            print >>sys.stderr, "Pairwise evaluation directory {0} already exists, skipping".format(curr_p3_dir)
                            continue

                        if not os.path.exists(parent):
                            os.makedirs(parent)

                        shutil.copytree(pairwise_skel_dir[treatment], "/tmp/fishjord_tmp_phase3_pairwise_skel/")
                        shutil.move("/tmp/fishjord_tmp_phase3_pairwise_skel/conf", curr_p3_dir)

                        pop1 = os.path.join(curr_p3_dir, "pop1.spop")
                        pop2 = os.path.join(curr_p3_dir, "pop2.spop")

                        out = open(pop1, "w")
                        cmd = [sample_script, "-r", "%s" % seed, "--set-lineage=1", "high", phase2_spop_pattern[ht].format(sgv, phase2_rep, seed_spop_update)]
                        print " ".join(cmd)
                        subprocess.check_call(cmd, stdout=out)
                        out.close()

                        out = open(pop2, "w")
                        cmd = [sample_script, "-r", "%s" % seed, "--set-lineage=2", "high", phase2_spop_pattern[ht_opp].format(sgv_opp, rep_opp, seed_spop_update)]
                        print " ".join(cmd)
                        subprocess.check_call(cmd, stdout=out)
                        out.close()

                        ## NOTE: Predator injects are already in the skeleton events-flat.cfg, they don't need to be inserted here since we're using handwritten predators in the evaluation
                        cmd = [sample_script, "-r", "%s" % seed, "--keep-lineage", "high", pop1, pop2]
                        print " ".join(cmd)
                        subprocess.check_call(cmd, stdout=open(os.path.join(curr_p3_dir, "seed.spop"), "w"))

                        cmd = ["sed", "-i", "s/{SEED}/%s/g" % random.randint(0, 5000000), os.path.join(curr_p3_dir, "avida.cfg")]
                        print " ".join(cmd)
                        subprocess.check_call(cmd)

                        cmd = ["sed", "-i", "s/{UPDATES}/11000/g", os.path.join(curr_p3_dir, "events-flat.cfg")]
                        print " ".join(cmd)
                        subprocess.check_call(cmd)

                        shutil.rmtree("/tmp/fishjord_tmp_phase3_pairwise_skel/")

print cnt

