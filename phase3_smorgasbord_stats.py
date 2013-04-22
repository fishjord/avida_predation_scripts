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

print "#rep_name\tupdate\tnum_prey\tprey_remaining%%"
for rep_dir in sys.argv[1:]:
    targets_file = os.path.join(rep_dir, "data/targets.dat")
    header, targets = avida_utils.read_avida_dat(targets_file)
    total_prey = float(targets[0][4] + targets[0][6] - (200 - targets[0][2]))

    for i in range(len(targets)):
        print "%s\t%s\t%s\t%f" % (rep_dir, targets[i]["Update"] - 1000, targets[i][4] + targets[i][6] - (200 - targets[i][2]), (targets[i][4] + targets[i][6] - (200 - targets[i][2])) / total_prey)
