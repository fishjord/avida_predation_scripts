#!/usr/bin/env python

import sys
import operator

if len(sys.argv) != 2:
    print >>sys.stderr, "USAGE: convert_lineage_ratios.txt <lineage_ratios.txt>"
    sys.exit(1)

counts = {}
counts["pred"] = {}
counts["nopred"] = {}

win_counts = {}
win_counts["pred"] = {}
win_counts["nopred"] = {}

sanity_check = {}

print "treatment\tinit_diversity_1\tpred_history_1\trep_1\tinit_diversity_2\tpred_history_2\trep_2\tupdate\ttotal_pop_size\tnum_lineage_1\tnum_lineage_2\tratio_lineage_1\tratio_lineage_2"
for line in open(sys.argv[1]):
    line = line.strip()
    if line[0] == "#" or line == "":
        continue
    #pairwise/treatment_nopred/clone_nopred_10__vs__clone_pred_29/data/detail-1000.spop
    lexemes = line.split("\t")
    path = lexemes[0].split("/")
    details = path[2].replace("__vs_", "").split("_")

    treatment = path[1].split("_")[1]
    sgv1 = details[0]
    ht1 = details[1]
    rep1 = details[2]
    sgv2 = details[3]
    ht2 = details[4]
    rep2 = details[5]
    update = int(lexemes[1]) - 1000

    if update == 10000:
        k1 = (sgv1, ht1)
        k2 = (sgv2, ht2)

        if k1 not in win_counts[treatment]:
            win_counts[treatment][k1] = {}
            counts[treatment][k1] = {}


        r1 = float(lexemes[-2])
        r2 = float(lexemes[-1])

        counts[treatment][k1][k2] = counts[treatment][k1].get(k2, 0) + 1
        if r1 > r2:
            win_counts[treatment][k1][k2] = win_counts[treatment][k1].get(k2, 0) + 1

    #if treatment == "pred":
    #    treatment = "PredatorPresent"
    #else:
    #    treatment = "PredatorAbsent"

    print "{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\t{8}".format(treatment, sgv1, ht1, rep1, sgv2, ht2, rep2, update, "\t".join(lexemes[2:]))

keys = sorted(win_counts["pred"].keys(), key=operator.itemgetter(1, 0))
c = {"pred" : 60.0, "nopred" : 59.0 }

for treatment in ["pred", "nopred"]:
    print >>sys.stderr, "{0} summary".format(treatment)
    s = ""
    for key in keys:
        s += "\t{0} {1}".format(*key)
    print >>sys.stderr, s

    for k1 in keys:
        s = "{0} {1}".format(*k1)
        for k2 in keys:
            s += "\t{0:.2f}".format(win_counts[treatment][k1].get(k2, 0) / float(counts[treatment][k1].get(k2, 1)))
        print >>sys.stderr, s

    print >>sys.stderr
