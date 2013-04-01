#!/usr/bin/python
import sys
import numpy
import re
import alignment
import avida_utils #make sure the avida_utils.py file is in the same directory as this script
                   #you can read that file, but it does contain some advanced python constructs

if len(sys.argv) < 2:
    print >>sys.stderr, "USAGE: compute_divergence.py <spop_file>..."
    sys.exit(1)

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

def compute_pop_ratios(spop):
    header, avida_data = avida_utils.read_avida_dat(spop)
    counts = {}
    ratios = {}

    for genotype in avida_data:
        num_units = genotype["Number of currently living organisms"]
        lineages = genotype["Lineage Label"]

        if "Z" in genotype["Genome Sequence"]:
            continue

        if type(lineages) != list:
            lineages = [lineages]

        for lineage in lineages:
            counts[lineage] = counts.get(lineage, 0) + 1

    tot_orgs = sum([counts[x] for x in counts])
    for lineage in counts:
        ratios[lineage] = counts[lineage] / float(tot_orgs)
        

    return tot_orgs, counts, ratios

if len(sys.argv) < 2:
    print "USAGE: compute_lineage_ratios.py <detail.spop>..."
    sys.exit(1)

update_number_regex = re.compile("(.+/)*detail-(\d+).spop")
print "#filename\tupdate\ttotal_pop_size\tnum_lineage_1\tnum_lineage_2\tratio_lineage_1\tratio_lineage_2"
for f in sys.argv[1:]:
    match = update_number_regex.match(f)
    if not match:
        raise Exception("Failed to find update number in file name '%s'" % f)
    update = int(match.groups()[1])

    tot_orgs, counts, ratios = compute_pop_ratios(f)

    if len(counts) > 2:
        print >>sys.stderr, "WARNING: %s contains an unexpected number of lineages" % f
    else:
        print "%s\t%s\t%s\t%s\t%s\t%s\t%s" % (f, update, tot_orgs, counts.get(1, 0), counts.get(2, 0), ratios.get(1, 0), ratios.get(2, 0))
