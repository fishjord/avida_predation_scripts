#!/usr/bin/python
#Python script to compute Shannon Diversity from .spop file and respective count found in the respective row of count.dat file. The update # could be grabbed from the filename, but can also be an input
#usage: python ShanDiv.py <population> <count.dat> [update number]
#sample usage: python ShanDiv.py detail-2000000.spop count.dat [2000000]

#The 2000000 is optional. Only include this number if file naming convention changes
#assuming the detail-#######.spop format


import avida_utils #make sure the avida_utils.py file is in the same directory as this script
                   #you can read that file, but it does contain some advanced python constructs
import sys
from math import log

def ShanDiversity(fname):
    """Calculate Shannon Diversity with formula SH_D = -sum(prob * log(prob)) """
    header,avida_data = avida_utils.read_avida_dat(fname)
    running_sum = 0

    genotype_cnts = []
    for genotype in avida_data:
        if "Z" in genotype["Genome Sequence"]:
            continue
        genotype_cnts.append(genotype["Number of currently living organisms"])

    population_size = float(sum(genotype_cnts))

    for i in range(len(genotype_cnts)):
        num_orgs = genotype_cnts[i]
        p = num_orgs / population_size
        running_sum += p * log(1/p,2) #Shannon's Diversity

    return population_size, running_sum

def main():
    if len(sys.argv) < 2:
        print >> sys.stderr, "usage: python ShanDiv.py [population]..."
        sys.exit(1)

    #nopred_replicates/clone/sim_10/data/detail-0.spop
    #init_diversity  pred_history    replicate       update
    print "init_diversity\tpred_history\treplicate\tupdate\tnum_prey\tshannon_diversity"
    for popFile in sys.argv[1:]:
        lexemes = popFile.split("/")
        hist_conting = lexemes[0].split("_")[0]

        if len(lexemes) == 5:
            sgv = lexemes[1]
            rep = lexemes[2].split("_")[1]
            update = lexemes[4].replace(".spop", "").split("-")[1]
        else:
            sgv = "NA"
            rep = lexemes[1].split("_")[1]
            update = lexemes[3].replace(".spop", "").split("-")[1]

        if hist_conting == "pred":
            hist_conting = "PredatorPresent"
        else:
            hist_conting = "PredatorAbsent"

        pop_size, diversity = ShanDiversity(popFile)
        print "{0}\t{1}\t{2}\t{3}\t{4}\t{5}".format(sgv, hist_conting, rep, update, pop_size, diversity)

if __name__ == "__main__":
    main()
