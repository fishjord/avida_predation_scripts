#!/usr/bin/python

import sys
import random
import copy
import avida_utils #make sure the avida_utils.py file is in the same directory as this script
                   #you can read that file, but it does contain some advanced python constructs

# Structured Population Save
# Fri Feb 15 18:31:22 2013
#  1: ID
#  2: Source
#  3: Source Args
#  4: Parent ID(s)
#  5: Number of currently living organisms
#  6: Total number of organisms that ever existed
#  7: Genome Length
#  8: Average Merit
#  9: Average Gestation Time
# 10: Average Fitness
# 11: Generation Born
# 12: Update Born
# 13: Update Deactivated
# 14: Phylogenetic Depth
# 15: Hardware Type ID
# 16: Inst Set Name
# 17: Genome Sequence
# 18: Occupied Cell IDs
# 19: Gestation (CPU) Cycle Offsets
# 20: Lineage Label
# 21: Current Group IDs
# 22: Current Forager Types
# 23: Birth Cells
# 24: Current Avatar Cell Locations
# 25: Avatar Birth Cell
# 26: Parent forager type
# 27: Was Parent a Teacher
# 28: Parent Merit

#Check to see if we have the right number of arguments
#by default the first argument is the script name
if len(sys.argv) != 2 and len(sys.argv) != 3:
    print "USAGE: sample_population.py <population file> [max orgs]"
    sys.exit(1)     #we don't have the information we need, exit with an error value

header, avida_data = avida_utils.read_avida_dat(sys.argv[1])  #Load the data from the file specified by the user

headers = list()
for line in open(sys.argv[1]):
    if line[0] == "#":
        headers.append(line.strip())
    else:
        break

print "%s" % ("\n".join(headers))
print

lineage = 0
for genotype in avida_data:
    num_units = genotype["Number of currently living organisms"]

    this_lineage = []
    for i in range(num_units):
        this_lineage.append("%s" % lineage)
        lineage += 1

    genotype["Lineage Label"] = ",".join(this_lineage)
    genotype["Parent ID(s)"] = "(none)"     #we need to clear the parent (re aaron)

    print avida_utils.format_line(header, genotype)
