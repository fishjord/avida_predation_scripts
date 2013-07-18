#!/usr/bin/python

import os
import random
import sys
import subprocess
import shutil

seed = 42
random.seed(seed)

#sample_script="/home/fishjord/documents/cse845/project/scripts/sample_population.py"
sample_script="/home/fishjord/cse845/scripts/sample_population.py"

#phase2_dir="/home/fishjord/documents/cse845/project/phase2"
phase2_dir="/mnt/scratch/fishjord/cse845_paper/evo_with_pred_phase/"
phase3_dir="."#"/home/fishjord/documents/cse845/project/phase3"

#sim_2m_13    1198    198     1644.83333333 avg look instructions
#predators_spop="/home/fishjord/documents/cse845/project/phase1/pred/sim_2m_13/data/detail-2000000.spop"
predators_spop="/mnt/scratch/fishjord/cse845_paper/hand_predators/lethal_predators.spop"

svgs = ["high", "intermediate", "clone"]
seed_pops = ["pred", "nopred"]

seed_replicates = {}

for svg in svgs:
    seed_replicates[svg] = {}
    for seed_pop in seed_pops:
        seed_replicates[svg][seed_pop] = random.randint(1, 30)

print "Selected replicates from phase 2 treatments: %s" % seed_replicates

p3_skels = {"pairwise" : os.path.join(phase3_dir, "skel/pairwise_skel"), 
            "solo" : os.path.join(phase3_dir, "skel/solo_skel"),
            "smorgasbord" : os.path.join(phase3_dir, "skel/smorgasbord_skel")}
p3_fpatterns = {"pairwise" : os.path.join(phase3_dir, "pairwise/%s/%s_%s_vs_%s_%s"), 
                "solo" : os.path.join(phase3_dir,"solo/%s/%s_%s"),
                "smorgasbord" : os.path.join(phase3_dir,"smorgasbord/%s_%s")}

phase2_spop_pattern = { "pred" : os.path.join(phase2_dir, "withpred_seed_pop/%s/sim_%s/data/detail-200000.spop"), 
                        "nopred" : os.path.join(phase2_dir, "nopred_seed_pop/%s/sim_%s/data/detail-200000.spop") }

for svg in svgs:
    for seed_pop in seed_pops:
        print "Preparing solo phase3 test %s %s" % (svg, seed_pop)
        for treatment in ["pred", "nopred"]:
            curr_p3_dir = p3_fpatterns["solo"] % (treatment, svg, seed_pop)
            parent = os.path.split(curr_p3_dir)[0]
            if not os.path.exists(parent):
                os.makedirs(parent)
            shutil.copytree(p3_skels["solo"], curr_p3_dir)
            cmd = [sample_script, "-r", "%s" % seed, "--keep-lineage", "high", phase2_spop_pattern[seed_pop] % (svg, seed_replicates[svg][seed_pop])]
            if treatment == "pred":
                cmd.insert(1, "--predators=%s" % predators_spop)
            print " ".join(cmd)
            subprocess.check_call(cmd, stdout=open(os.path.join(curr_p3_dir, "conf/seed.spop"), "w"))

        print "Preparing smorgasbord phase3 test %s %s" % (svg, seed_pop)
        curr_p3_dir = p3_fpatterns["smorgasbord"] % (svg, seed_pop)
        parent = os.path.split(curr_p3_dir)[0]
        if not os.path.exists(parent):
            os.makedirs(parent)
        shutil.copytree(p3_skels["smorgasbord"], curr_p3_dir)
        cmd = [sample_script, "-r", "%s" % seed, "--keep-lineage", "high", phase2_spop_pattern[seed_pop] % (svg, seed_replicates[svg][seed_pop])]
        cmd.insert(1, "--predators=%s" % predators_spop)
        print " ".join(cmd)
        subprocess.check_call(cmd, stdout=open(os.path.join(curr_p3_dir, "conf/seed.spop"), "w"))

        print "\nPreparing pairwise phase3 competitions for treatment %s %s" % (svg, seed_pop)
        for svg_opp in svgs:
            for seed_pop_opp in seed_pops:
                if svg == svg_opp and seed_pop == seed_pop_opp:
                    continue

                for treatment in ["pred", "nopred"]:
                    curr_p3_dir = p3_fpatterns["pairwise"] % (treatment, svg, seed_pop, svg_opp, seed_pop_opp)
                    parent = os.path.split(curr_p3_dir)[0]
                    if not os.path.exists(parent):
                        print parent
                        os.makedirs(parent)
                    shutil.copytree(p3_skels["pairwise"], curr_p3_dir)

                    pop1 = os.path.join(curr_p3_dir, "pop1.spop")
                    pop2 = os.path.join(curr_p3_dir, "pop2.spop")

                    out = open(pop1, "w")
                    cmd = [sample_script, "-r", "%s" % seed, "--set-lineage=1", "high", phase2_spop_pattern[seed_pop] % (svg, seed_replicates[svg][seed_pop])]
                    print " ".join(cmd)
                    subprocess.check_call(cmd, stdout=out)
                    out.close()

                    out = open(pop2, "w")
                    cmd = [sample_script, "-r", "%s" % seed, "--set-lineage=2", "high", phase2_spop_pattern[seed_pop_opp] % (svg_opp, seed_replicates[svg_opp][seed_pop_opp])]
                    print " ".join(cmd)
                    subprocess.check_call(cmd, stdout=out)
                    out.close()

                    cmd = [sample_script, "-r", "%s" % seed, "--keep-lineage", "high", pop1, pop2]

                    if treatment == "pred":
                        cmd.insert(1, "--predators=%s" % predators_spop)
                    print " ".join(cmd)
                    subprocess.check_call(cmd, stdout=open(os.path.join(curr_p3_dir, "conf/seed.spop"), "w"))

