#!/usr/bin/env python

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
from avida_utils import list_if_not
import argparse
import avida_utils #make sure the avida_utils.py file is in the same directory as this script
                   #you can read that file, but it does contain some advanced python constructs

file_header = """#filetype genotype_data
#format id src src_args parents num_units total_units length merit gest_time fitness gen_born update_born update_deactivated depth hw_type inst_set sequence cells gest_offset lineage group_id forager_type birth_cell avatar_cell av_bcell parent_ft parent_is_teach parent_merit
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
"""

def random_pick(v):
    if type(v) == list:
        return random.choice(v)
    else:
        return v

def read_pred_only(fname):
    header, avida_data = avida_utils.read_avida_dat(fname)
    ret = []
    cnt = 0

    for genotype in avida_data:
        forager_types = genotype["Current Forager Types"]
        parent_ft = genotype["Parent forager type"]
        if type(forager_types) != list:
            forager_types = [forager_types]
        if type(parent_ft) != list:
            parent_ft = [parent_ft]

        if "Z" not in genotype["Genome Sequence"]:
            continue
        if -2 not in forager_types and -2 not in parent_ft:
            continue

        cnt += genotype["Number of currently living organisms"]

        genotype["Parent ID(s)"] = "(none)"
        genotype["Current Forager Types"] = [-2] * genotype["Number of currently living organisms"]
        genotype["Parent forager type"] = [-2] * genotype["Number of currently living organisms"]
        genotype["Was Parent a Teacher"] = [1] * genotype["Number of currently living organisms"]

        ret.append(genotype)

    return header, ret, cnt

def read_and_tweakspop(fname):
    header, avida_data = avida_utils.read_avida_dat(fname)
    ret = []
    cnt = 0

    for genotype in avida_data:
        forager_types = genotype["Current Forager Types"]
        parent_ft = genotype["Parent forager type"]
        if type(forager_types) != list:
            forager_types = [forager_types]
        if type(parent_ft) != list:
            parent_ft = [parent_ft]

        if -2 in forager_types or -2 in parent_ft:
            continue

        cnt += genotype["Number of currently living organisms"]

        genotype["Genome Sequence"] = genotype["Genome Sequence"].replace("Z", "3")
        genotype["Parent ID(s)"] = "(none)"

        ret.append(genotype)


    return header, ret, cnt

def find_free_cell(taken_cells, seed):
    change = -1
    cell = seed
    while cell in taken_cells:
        cell += change
        if cell < 1:
            cell = seed
            change = 1
        elif cell > 251*251:   # We use a 251 by 251 grid, so if we didn't find a free cell between 0-seed nor seed-255^2...
            raise Exception("Probably a problem finding an empty cell...")

    taken_cells.add(cell)

    return cell

def find_free_random_cell(taken_cells):
    cell = random.randint(1, 251*251)
    while cell in taken_cells:
        cell = random.randint(1, 251*251)

    taken_cells.add(cell)

    return cell

def create_org_from_template(template, replicates, org_id, taken_cells, lineage, pred=False):
    org = copy.deepcopy(template)
    org["ID"] = org_id
    num_units = org["Number of currently living organisms"]
    org["Number of currently living organisms"] = replicates
    org["Total number of organisms that ever existed"] = replicates
    #try to find a place as close as possible to where they were originally

    if type(lineage) == bool and lineage == True:
        pass #leave lineage alone
    elif type(lineage) == int:
        org["Lineage Label"] = [lineage] * replicates
    else:
        org["Lineage Label"] = [org_id] * replicates

    """
    I had trouble deciding the best way to replicate an organism more (or less) times than how many were alive at the time the
    population snapshot was taken.  I've settled on randomly selecting one of the values from a living organism for every
    replicate.
    """
    troublesome_attrs = ["Occupied Cell IDs", "Gestation (CPU) Cycle Offsets", "Current Group IDs", "Current Forager Types", "Birth Cells", "Current Avatar Cell Locations", "Avatar Birth Cell", "Parent forager type", "Was Parent a Teacher", "Parent Merit"]
    for attr in troublesome_attrs:
        org[attr] = []

    for i in range(replicates):
        for attr in troublesome_attrs:
            v = random_pick(template[attr])
            if attr == "Current Forager Types":
                if pred:
                    org[attr].append(-2)
                else:
                    org[attr].append(0)
            elif attr == "Parent forager type":
                if pred:
                    org[attr].append(-2)
                else:
                    org[attr].append(0)
            elif "cell" in attr.lower():
                #for cells we have to be careful not to duplicate values 
                if attr not in taken_cells:
                    taken_cells[attr] = set()
                    
                if taken_cells["rand"]:
                    org[attr].append(find_free_random_cell(taken_cells[attr]))
                else:
                    org[attr].append(find_free_cell(taken_cells[attr], v))
            else:
                #for the other ones we (should) be fine with duplicate values
                org[attr].append(v)

    return org

def write_pred(predators, header, taken_cells):
    org_id = len(taken_cells.get("Birth Cells", [])) + 1
    for predator in predators:
        print avida_utils.format_line(header, create_org_from_template(predator, predator["Number of currently living organisms"], org_id, taken_cells, None, pred=True))
        org_id += 1

def write_high(avida_data, header, lineage, taken_cells):
    for i in range(len(avida_data)):
        org = avida_data[i]            
        print avida_utils.format_line(header, create_org_from_template(org, org["Number of currently living organisms"], i, taken_cells, lineage))

def write_intermediate(avida_data, header, num_output, replicates, lineage, taken_cells):
    genotypes = {}
    for i in range(0, num_output, replicates):
        org = random.choice(avida_data)
        genome = org["Genome Sequence"]
        if genome not in genotypes:
            genotypes[genome] = {"cnt" : 0, "template" : org}

        genotypes[genome]["cnt"] += min(replicates, num_output - i) # make sure we don't accidently create too many organisms

    org_id = 1
    for genome in genotypes:
        genotype = genotypes[genome]
        print avida_utils.format_line(header, create_org_from_template(genotype["template"], genotype["cnt"], org_id, taken_cells, lineage))
        org_id += 1

def write_clone(avida_data, header, num_output, lineage, taken_cells):
    print >>sys.stderr, "Writing out %s clones" % num_output
    print avida_utils.format_line(header, create_org_from_template(random.choice(avida_data), num_output, 1, taken_cells, lineage))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--random-seed", dest="seed", help="Set the random number seed", default=0, type=int)
    parser.add_argument("--random-loc", dest="rand_loc", default=False, action="store_true")
    parser.add_argument("--replicates", dest="replicates", help="Set the random number of replicates for the intermediate mode", default=55, type=int)
    parser.add_argument("--predators", dest="predators", help="Load predators from this spop")
    parser.add_argument("mode", help="Selection mode", choices=set(["high", "intermediate", "clone"]))

    g = parser.add_mutually_exclusive_group(required=False)
    g.add_argument("--set-lineage", dest="lineage", type=int, help="Set all output organism lineages to this value")
    g.add_argument("--keep-lineage", dest="keep_lineage", action="store_true", help="Keep organism lineages from seed populations")

    parser.add_argument("seed_population", nargs="+")

    args = parser.parse_args()

    print >>sys.stderr, "Setting random seed to %s" % args.seed
    random.seed(args.seed)

    sample_type = args.mode

    taken_cells = {}
    tot_prey = 0

    if args.lineage:
        lineage = args.lineage
    elif args.keep_lineage:
        lineage = True
    else:
        lineage = None

    taken_cells["rand"] = args.rand_loc
    

    print file_header
    for seed_pop in args.seed_population:
        header, avida_data, num_prey = read_and_tweakspop(seed_pop)  #Load the data from the file specified by the user    
        tot_prey += num_prey

        if sample_type == "high":
            write_high(avida_data, header, lineage, taken_cells)
        elif sample_type.startswith("intermediate"):
            replicates = args.replicates
            print >>sys.stderr, "Intermediate population replicate number: %d" % args.replicates
            write_intermediate(avida_data, header, num_prey, replicates, lineage, taken_cells)
        elif sample_type == "clone":
            write_clone(avida_data, header, num_prey, lineage, taken_cells)

    if args.predators:
        header, predators, num_pred = read_pred_only(args.predators)
        print >>sys.stderr, "Writing predators %s from %s" % (args.predators, num_pred)
        write_pred(predators, header, taken_cells)
    else:
        num_pred = 0

    print >>sys.stderr, "Read in %s organisms from %s and created a(n) %s variation spop file with %s predators" % (tot_prey, args.seed_population, args.mode, num_pred)
    for taken in taken_cells:
        if taken == "rand":
            continue
        print >>sys.stderr, taken, len(taken_cells[taken])


if __name__ == "__main__":
    main()
