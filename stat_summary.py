#!/usr/bin/env python

import sys
import numpy
import operator

if len(sys.argv) != 3:
    print >>sys.stderr, "USAGE: stats_summary.py <update_column> <solo_stat_file>"
    sys.exit(1)

update_column = int(sys.argv[1])

running_averages = {}
headers = None
for line in open(sys.argv[2]):
    if line[0] == "#":
        if headers != None:
            raise Exception("Multiple header lines!")
        headers = line.strip()[1:].split("\t")
        continue

    if headers == None:
        raise Exception("No header line!")

    line = line.replace("\t\t", "\t")

    #evaluation      treatment       sgv     hist_contig     replicate       update  num_prey        ratio_moves     ratio_looks     ratio_rotate    tot_prey_insts  num_pred        pred_attacks
    #solo    nopred  clone   nopred  1               1000    1000    1.01871260167e-05       2.19402791214e-05       1.0858280483e-05        4465440 0       0
    lexemes = line.strip().split("\t")
    if len(lexemes) != len(headers):
        print len(lexemes)
        continue

    key = " ".join(lexemes[:update_column - 1])
    update = int(lexemes[update_column])
    key = (key, update)

    if key not in running_averages:
        running_averages[key] = {}
        for header in headers[update_column+1:]:
            running_averages[key][header] = []

    for i in range(update_column + 1, len(lexemes)):
        running_averages[key][headers[i]].append(float(lexemes[i]))

print "treatment\tupdate\t{0}".format("\t".join(["{0}_mean\t{0}_std".format(header) for header in headers[update_column + 1:]]))
for key in sorted(running_averages.keys(), key=operator.itemgetter(1, 0)):
    s = "{0}\t{1}\t".format(key[0], key[1])
    for header in headers[update_column + 1:]:
        arr = running_averages[key][header]
        s += "{0:.3f}\t{1:.3f}\t".format(numpy.mean(arr), numpy.std(arr))
        
    print s
