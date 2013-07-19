#!/usr/bin/python

import os
import random
import sys
import subprocess
import shutil

seed = 42
random.seed(seed)

sample_script=os.path.join(os.path.split(os.path.abspath(__file__))[0], "sample_population.py")

if len(sys.argv) != 4:
    print >>sys.stderr, "USAGE: evaluation_replicate_generation.py <phase2_dir> <evaluation_out_dir> <population_from_update>"
    sys.exit(1)

phase2_dir=sys.argv[1]
phase3_dir=sys.argv[2]
seed_spop_update = sys.argv[3]

sgvs = ["high", "intermediate", "clone"]
hist_contings = ["pred", "nopred"]

solo_skel_dir = { "pred" : os.path.join(phase3_dir, "skel/solo_skel_pred"), "nopred" : os.path.join(phase3_dir, "skel/solo_skel_nopred")}
solo_eval_path_pattern = os.path.join(phase3_dir,"solo/treatment_{0}/sgv_{1}_histconting_{2}/sim_{3}")

phase2_spop_pattern = { "pred" : os.path.join(phase2_dir, "pred_replicates/{0}/sim_{1}/data/detail-{2}.spop"), 
                        "nopred" : os.path.join(phase2_dir, "nopred_replicates/{0}/sim_{1}/data/detail-{2}.spop") }

for sgv in sgvs:
    for hist_conting in hist_contings:
        for treatment in ["pred", "nopred"]:
            for phase2_rep in range(1, 31):
                print "Preparing solo phase3 test %s %s" % (sgv, hist_conting)
                curr_p3_dir = solo_eval_path_pattern.format(treatment, sgv, hist_conting, phase2_rep)
                parent = os.path.split(curr_p3_dir)[0]

                if os.path.exists(curr_p3_dir):
                    print >>sys.stderr, "Solo evaluation directory {0} already exists, skipping".format(curr_p3_dir)

                if not os.path.exists(parent):
                    os.makedirs(parent)

                shutil.copytree(solo_skel_dir[treatment], "/tmp/fishjord_tmp_phase3_solo_skel/")
                shutil.move("/tmp/fishjord_tmp_phase3_solo_skel/conf", curr_p3_dir)

                ## NOTE: Predator injects are already in the skeleton events-flat.cfg, they don't need to be inserted here since we're using handwritten predators in the evaluation
                cmd = [sample_script, "-r", str(seed), "--keep-lineage", "high", phase2_spop_pattern[hist_conting].format(sgv, phase2_rep, seed_spop_update)]
                print " ".join(cmd)
                subprocess.check_call(cmd, stdout=open(os.path.join(curr_p3_dir, "seed.spop"), "w"))

                cmd = ["sed", "-i", "s/{SEED}/%s/g" % random.randint(0, 5000000), os.path.join(curr_p3_dir, "avida.cfg")]
                print " ".join(cmd)
                subprocess.check_call(cmd)

                cmd = ["sed", "-i", "s/{UPDATES}/11000/g", os.path.join(curr_p3_dir, "events-flat.cfg")]
                print " ".join(cmd)
                subprocess.check_call(cmd)

                shutil.rmtree("/tmp/fishjord_tmp_phase3_solo_skel/")
