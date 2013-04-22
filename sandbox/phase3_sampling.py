#!/usr/bin/python

import os
import random
import sys
import subprocess
import shutil

seed = 42
random.seed(seed)

#sample_script="/home/fishjord/documents/cse845/project/scripts/sample_population.py"
sample_script="/home/fishjord/cse845/avida_predation_scripts/sample_population.py"

#phase2_dir="/home/fishjord/documents/cse845/project/phase2"
phase2_dir="/mnt/scratch/fishjord/phase2"
phase3_dir="."#"/home/fishjord/documents/cse845/project/phase3"

#sim_2m_13    1198    198     1644.83333333 avg look instructions
#predators_spop="/home/fishjord/documents/cse845/project/phase1/pred/sim_2m_13/data/detail-2000000.spop"
predators_spop="/home/fishjord/cse845/predator_sim/sim_2m_13/data/detail-2000000.spop"

svgs = ["high", "intermediate", "clone"]
seed_pops = ["pred", "nopred"]

seed_replicates = {}

for svg in svgs:
    seed_replicates[svg] = {}
    for seed_pop in seed_pops:
        seed_replicates[svg][seed_pop] = random.randint(1, 30)

print "Selected replicates from phase 2 treatments: %s" % seed_replicates

p3_skels = {"pairwise" : os.path.join(phase3_dir, "skel/pairwise_skel"), "solo" : os.path.join(phase3_dir, "skel/solo_skel")}
p3_fpatterns = {"pairwise" : os.path.join(phase3_dir, "pairwise_%s_%s_vs_%s_%s_with%s"), "solo" : os.path.join(phase3_dir,"solo_%s_%s_with%s")}

phase2_spop_pattern = os.path.join(phase2_dir, "%s_%s_phase2/sim_200000_%s/data/detail-0.spop")

for svg in svgs:
    for seed_pop in seed_pops:
        print "Preparing solo phase3 test %s %s" % (svg, seed_pop)
        for treatment in ["pred", "nopred"]:
            curr_p3_dir = p3_fpatterns["solo"] % (svg, seed_pop, treatment)
            shutil.copytree(p3_skels["solo"], curr_p3_dir)
            cmd = [sample_script, "-r", "%s" % seed, "--keep-lineage", "high", phase2_spop_pattern % (svg, seed_pop, seed_replicates[svg][seed_pop])]
            if treatment == "pred":
                cmd.insert(1, "--predators=%s" % predators_spop)
            print " ".join(cmd)
            subprocess.check_call(cmd, stdout=open(os.path.join(curr_p3_dir, "conf/seed.spop"), "w"))

        print "\nPreparing pairwise phase3 competitions for treatment %s %s" % (svg, seed_pop)
        for svg_opp in svgs:
            for seed_pop_opp in seed_pops:
                if svg == svg_opp and seed_pop == seed_pop_opp:
                    continue

                for treatment in ["pred", "nopred"]:
                    curr_p3_dir = p3_fpatterns["pairwise"] % (svg, seed_pop, svg_opp, seed_pop_opp, treatment)
                    shutil.copytree(p3_skels["pairwise"], curr_p3_dir)

                    pop1 = os.path.join(curr_p3_dir, "pop1.spop")
                    pop2 = os.path.join(curr_p3_dir, "pop2.spop")

                    out = open(pop1, "w")
                    cmd = [sample_script, "-r", "%s" % seed, "--set-lineage=1", "high", phase2_spop_pattern % (svg, seed_pop, seed_replicates[svg][seed_pop])]
                    print " ".join(cmd)
                    subprocess.check_call(cmd, stdout=out)
                    out.close()

                    out = open(pop2, "w")
                    cmd = [sample_script, "-r", "%s" % seed, "--set-lineage=2", "high", phase2_spop_pattern % (svg_opp, seed_pop_opp, seed_replicates[svg_opp][seed_pop_opp])]
                    print " ".join(cmd)
                    subprocess.check_call(cmd, stdout=out)
                    out.close()

                    cmd = [sample_script, "-r", "%s" % seed, "--keep-lineage", "high", pop1, pop2]

                    if treatment == "pred":
                        cmd.insert(1, "--predators=%s" % predators_spop)
                    print " ".join(cmd)
                    subprocess.check_call(cmd, stdout=open(os.path.join(curr_p3_dir, "conf/seed.spop"), "w"))

