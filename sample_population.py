#!/usr/bin/python

"""
The first line of this file (#!/usr/bin/python) tells our shell how to 
run this file so we can simply type ./sample_population.py and have it
be equivelent to typing 'python sample_population.py' 
"""

"""
In python you can specify comments in two ways, the triple quotes means
that everything until the next triple quote is a comment
"""

#we can also do single line comments by using the # sign

"""
most python files will start with a set of imports, basically listing
what modules we intend to use

two common imports are 'sys' and 'os'
"""
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

def replicate_population(avida_data):
    population = list()  #our population, which will contain one prey organism

    lineage = 0
    for genotype in avida_data:
        forager_types = genotype["Current Forager Types"]
        if type(forager_types) != list:
            forager_types = [forager_types]

        if -2 in forager_types:
            continue

        parent_ft = genotype["Parent forager type"]
        if type(parent_ft) != list:
            parent_ft = [parent_ft]

        if -2 in parent_ft:
            continue

        genotype["Genome Sequence"] = genotype["Genome Sequence"].replace("Z", "3")
        #if "Z" in genotype["Genome Sequence"]:
        #    continue

        num_units = genotype["Number of currently living organisms"]
        for i in range(num_units): # for every copy of this genotype
            org = copy.deepcopy(genotype)

            for j in org:
                if type(org[j]) == list:
                    if len(org[j]) == num_units:
                        org[j] = org[j][i]
                    else:
                        org[j] = ",".join(org[j])

            org["Parent ID(s)"] = "(none)"     #we need to clear the parent (re aaron)
            org["Lineage Label"] = lineage
            lineage += 1

            population.append(org)

    return population

#Check to see if we have the right number of arguments
#by default the first argument is the script name
if len(sys.argv) != 2 and len(sys.argv) != 3:
    print "USAGE: sample_population.py <population file> [max orgs]"
    sys.exit(1)     #we don't have the information we need, exit with an error value

header, avida_data = avida_utils.read_avida_dat(sys.argv[1])  #Load the data from the file specified by the user
population = replicate_population(avida_data)

headers = list()
for line in open(sys.argv[1]):
    if line[0] == "#":
        headers.append(line.strip())
    else:
        break

print "%s" % ("\n".join(headers))
print

num_output = len(population)
if len(sys.argv) == 3:
    num_output = int(sys.argv[2])

taken_cells = set()
for i in range(num_output):
    org = random.choice(population)
    org["ID"] = i
    org["Number of currently living organisms"] = 1
    cell = org["Birth Cells"]

    change = -1
    while cell in taken_cells:
        cell += change
        if cell < 1:
            cell = org["Birth Cells"]
            change = 1

    org["Birth Cells"] = cell

    print avida_utils.format_line(header, org)
