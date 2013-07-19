#!/usr/bin/python

import avida_utils
import os
import sys

"""
# 45: move
# 46: get-north-offset
# 47: rotate-x
# 48: rotate-org-id
# 49: rotate-away-org-id
# 50: set-forage-target
# 51: get-forage-target
# 52: look-ahead-intercept
# 53: attack-prey
# 54: attack-pred
"""

if len(sys.argv) < 2:
    print >>sys.stderr, "solo_stats.py <phase2|phase3> <rep_directory>..."
    sys.exit(1)

phase = sys.argv[1]

#solo/treatment_pred/sgv_intermediate_histconting_pred/sim_8

if phase == "phase3":
    sys.stdout.write("treatment\t")
    last_expected_update = 11000
    update_step = 500
else:
    last_expected_update = 200000
    update_step = 1000

print "init_diversity\tpred_history\treplicate\tupdate\tnum_prey\tmoves\tlooks\trotate\tprey_insts\tnum_pred\tpred_attacks"
expected_pred = 200
for rep_dir in sys.argv[2:]:
    lexemes = rep_dir.split("/")
    if phase == "phase3":
        if len(lexemes) != 4:
            continue

        eval_treatment = lexemes[1].split("_")[-1]
        sgv = lexemes[2].split("_")[1]
        hist_conting = lexemes[2].split("_")[3]
        rep = lexemes[3].split("_")[1]
    else:
        if len(lexemes) != 3:
            continue
        eval_treatment = None
        hist_conting = lexemes[0].split("_")[0]
        sgv = lexemes[1].split("_")[0]
        rep = lexemes[2].split("_")[1]

    targets_file = os.path.join(rep_dir, "data/targets.dat")
    pred_inst_file = os.path.join(rep_dir, "data/count.dat")
    prey_inst_file = os.path.join(rep_dir, "data/prey_instruction.dat")

    if not os.path.exists(os.path.join(rep_dir, "submitted")):
        continue

    if not os.path.exists(os.path.join(rep_dir, "data")):
        print >>sys.stderr, "ERROR\t{0}\tNo data directory".format(rep_dir)
        continue

    expected_updates = set(range(0, last_expected_update + 1, update_step))

    if not os.path.exists(os.path.join(rep_dir, "data/targets.dat")):
        continue

    if phase == "phase3":
        treatment = eval_treatment
    else:
        treatment = hist_conting

    if treatment == "pred":
        treatment = "PredatorPresent"
    else:
        treatment = "PredatorAbsent"

    try:
        header, targets = avida_utils.read_avida_dat(targets_file)
        header, prey_inst = avida_utils.read_avida_dat(prey_inst_file)
        header, pred_inst = avida_utils.read_avida_dat(pred_inst_file)
        if len(targets) != len(prey_inst) or len(prey_inst) != len(pred_inst):
            print >>sys.stderr, "ERROR\t{0}\tNumber of updates in targets/prey/pred inst not the same".format(rep_dir)
            continue

        for i in range(len(targets)):
            instructions = 0.0
            for x in prey_inst[i].keys():
                if type(x) != int and x != "Update":
                    instructions += prey_inst[i][x]

            num_pred = targets[i][2]
            num_prey = targets[i][4] + targets[i][6]
            update = targets[i]["Update"]

            if update not in expected_updates:
                print >>sys.stderr, "WARNING\t{0}\tUpdate {1} is not an expected update, skipping".format(rep_dir, update)
                continue

            if num_prey < 900:
                print >>sys.stderr, "WARNING\t{0}\tAbnormally low prey count update {1}".format(rep_dir, update)
            expected_updates.remove(update)

            if phase == "phase3":
                if eval_treatment == "pred" and num_pred != expected_pred:
                    print >>sys.stderr, "WARNING\t{0}\t{1} predators".format(rep_dir, expected_pred)

                print "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % (treatment, sgv, hist_conting, rep, update - 1000, num_prey, prey_inst[i]["move"], prey_inst[i]["look-ahead-intercept"], prey_inst[i]["rotate-x"], int(instructions), targets[i][2], pred_inst[i]["Total Attacks"])
            else:
                print "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % (sgv, treatment, rep, update, num_prey, prey_inst[i]["move"], prey_inst[i]["look-ahead-intercept"], prey_inst[i]["rotate-x"], int(instructions), targets[i][2], pred_inst[i]["Total Attacks"])

    except Exception as e:
        print >>sys.stderr, "ERROR\t{0}\t{1}".format(rep_dir, e)
        continue
    finally:
        if len(expected_updates) > 0:
            print >>sys.stderr, "WARNING\t{0}\tMissing data for updates {1}".format(rep_dir, expected_updates)
            for update in sorted(expected_updates):
                if phase == "phase3":
                    print "{0}\t{1}\t{2}\t{3}\t{4}\t0\t0\t0\t0\t0\t0\t0".format(treatment, sgv, hist_conting, rep, update - 1000)
                else:
                    print "{0}\t{1}\t{2}\t{3}\t0\t0\t0\t0\t0\t0\t0".format(sgv, treatment, rep, update)

