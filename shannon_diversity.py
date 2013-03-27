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

    print "#input_file\tpopulation_size(prey)\tshannon_diversity"
    for popFile in sys.argv[1:]:
        pop_size, diversity = ShanDiversity(popFile)
        print "%s\t%s\t%s" % (popFile, pop_size, diversity)

if __name__ == "__main__":
    main()
