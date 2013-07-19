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
    print >>sys.stderr, "phase3_solo_stats.py <rep_directory>..."
    sys.exit(1)

#solo/treatment_pred/sgv_intermediate_histconting_pred/sim_8
print "#treatment\tinit_diversity\tpred_history\treplicate\tupdate\tnum_prey\tmoves\tlooks\trotate\tprey_insts\tnum_pred\tpred_attacks"
expected_pred = 200
for rep_dir in sys.argv[1:]:
    lexemes = rep_dir.split("/")
    if len(lexemes) != 4:
        continue

    eval_treatment = lexemes[1].split("_")[-1]
    sgv = lexemes[2].split("_")[1]
    hist_conting = lexemes[2].split("_")[3]
    rep = lexemes[3].split("_")[1]

    targets_file = os.path.join(rep_dir, "data/targets.dat")
    pred_inst_file = os.path.join(rep_dir, "data/count.dat")
    prey_inst_file = os.path.join(rep_dir, "data/prey_instruction.dat")

    if not os.path.exists(os.path.join(rep_dir, "submitted")):
        continue

    if not os.path.exists(os.path.join(rep_dir, "data")):
        print >>sys.stderr, "ERROR\t{0}\tNo data directory".format(rep_dir)
        continue

    expected_updates = set(range(1000, 10500, 500))

    if not os.path.exists(os.path.join(rep_dir, "data/targets.dat")):
        if os.path.exists(os.path.join(rep_dir, "completed")):
            print >>sys.stderr, "WARNING\t{0}\tData dir exists, completed file exists, not targets, assuming extinct pop loaded".format(rep_dir)
            for update in sorted(expected_updates):
                print "{0}\t{1}\t{2}\t{3}\t{4}\t0\t0\t0\t0\t0\t0\t0".format(eval_treatment, sgv, hist_conting, rep, update - 1000)
        else:
            print >>sys.stderr, "ERROR\t{0}\tBorked directory structure".format(rep_dir)
        continue

    try:
        header, targets = avida_utils.read_avida_dat(targets_file)
        header, prey_inst = avida_utils.read_avida_dat(prey_inst_file)
        header, pred_inst = avida_utils.read_avida_dat(pred_inst_file)
    except Exception as e:
        print >>sys.stderr, "ERROR\t{0}\t{1}".format(rep_dir, e)
        continue

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

        if eval_treatment == "pred" and num_pred != expected_pred:
            print >>sys.stderr, "WARNING\t{0}\t{1} predators".format(rep_dir, expected_pred)

        if eval_treatment == "pred":
            treatment = "PredatorPresent"
        else:
            treatment = "PredatorAbsent"

        print "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % (treatment, sgv, hist_conting, rep, update - 1000, num_prey, prey_inst[i]["move"], prey_inst[i]["look-ahead-intercept"], prey_inst[i]["rotate-x"], int(instructions), targets[i][2], pred_inst[i]["Total Attacks"])

    if len(expected_updates) > 0:
        print >>sys.stderr, "WARNING\t{0}\tMissing data for updates {1}".format(rep_dir, expected_updates)
        for update in sorted(expected_updates):
            print "{0}\t{1}\t{2}\t{3}\t{4}\t0\t0\t0\t0\t0\t0\t0".format(eval_treatment, sgv, hist_conting, rep, update - 1000)
