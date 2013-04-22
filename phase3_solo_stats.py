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

print "#rep_name\tupdate\tnum_prey\tprey_moves\tprey_looks\tprey_rotate\tnum_preds\tpred_attacks"
for rep_dir in sys.argv[1:]:
    targets_file = os.path.join(rep_dir, "data/targets.dat")
    pred_inst_file = os.path.join(rep_dir, "data/predator_instruction.dat")
    prey_inst_file = os.path.join(rep_dir, "data/prey_instruction.dat")

    try:
        header, targets = avida_utils.read_avida_dat(targets_file)
        header, prey_inst = avida_utils.read_avida_dat(prey_inst_file)
        header, pred_inst = avida_utils.read_avida_dat(pred_inst_file)
    except Exception as e:
        print >>sys.stderr, "Error when reading data files for %s: %s" % (rep_dir, e)
        continue

    if len(targets) != len(prey_inst) or len(prey_inst) != len(pred_inst):
        print >>sys.stderr, "Number of updates in targets/prey/pred inst not the same"
        continue

    for i in range(len(targets)):
        print "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % (rep_dir, targets[i]["Update"], targets[i][4] + targets[i][6], prey_inst[i]["move"], prey_inst[i]["look-ahead-intercept"], prey_inst[i]["rotate-x"], targets[i][2], pred_inst[i]["attack-prey"])
