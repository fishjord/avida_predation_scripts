#!/usr/bin/python
import sys
import numpy
import re
import alignment
import avida_utils #make sure the avida_utils.py file is in the same directory as this script
                   #you can read that file, but it does contain some advanced python constructs

if len(sys.argv) < 3:
    print >>sys.stderr, "USAGE: compute_divergence.py <seed_population> <spop_file>..."
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

alignment_cache = dict()

def compute_dist(genome1, genome2):
    if genome1 in alignment_cache and genome2 in alignment_cache[genome1]:
        aln1, aln2, score = alignment_cache[genome1][genome2]
    else:
        aln1, aln2, score = alignment.global_alignment(genome1, genome2, 0, -1, -1)
        if genome1 not in alignment_cache:
            alignment_cache[genome1] = dict()
        if genome2 not in alignment_cache:
            alignment_cache[genome2] = dict()

        alignment_cache[genome1][genome2] = alignment_cache[genome2][genome1] = (aln1, aln2, score)
    #print "ancestor genome:",aln1
    #print "curr_genome:    ",aln2

    if len(aln1) != len(aln2):
        raise Exception("Genome lengths don't match")

    mismatches = 0.0
    for i in range(len(aln1)):
        if aln1[i] != aln2[i]:
            mismatches += 1

    return mismatches / len(aln1)

def load_divergence(spop, seed_genome, only_lineages = None):
    header, avida_data = avida_utils.read_avida_dat(spop)
    organism_divergences = []

    for genotype in avida_data:
        num_units = genotype["Number of currently living organisms"]
        lineages = genotype["Lineage Label"]

        if "Z" in genotype["Genome Sequence"]:
            continue

        if type(lineages) != list:
            lineages = [lineages]
        for lineage in lineages:

            if only_lineages != None and lineage not in only_lineages:
                continue

            best_dist = 1
            for seed_genome in seed_genomes[lineage]:
                best_dist = min(compute_dist(seed_genome, genotype["Genome Sequence"]), best_dist)

            organism_divergences.append(best_dist)

    return organism_divergences

only_lineages = None
if sys.argv[1] == "-l":
    only_lineages = [int(x) for x in sys.argv[2].split(",")]
    args =  sys.argv[3:]
else:
    args = sys.argv[1:]

if len(args) < 2:
    print "USAGE: sample_population.py [-l only,these,lineage,labels] <seed population> <detail.spop>..."
    sys.exit(1)

header, avida_data = avida_utils.read_avida_dat(args[0])  #Load the data from the file specified by the user

seed_genomes = dict()

for genotype in avida_data:
    lineages = genotype["Lineage Label"]
    if type(lineages) != list:
        lineages = [lineages]
    for lineage in lineages:
        if lineage not in seed_genomes:
            seed_genomes[lineage] = list()
            seed_genomes[lineage].append(genotype["Genome Sequence"])
        else:
            print >>sys.stderr, "WARNING: multiple organisms have lineage %s" % lineage


spop_data = []
update_number_regex = re.compile("(.+/)*detail-(\d+).spop")

for f in args[1:]:
    match = update_number_regex.match(f)
    if not match:
        raise Exception("Failed to find update number in file name '%s'" % f)
    update = int(match.groups()[1])

    divergences = load_divergence(f, seed_genomes, only_lineages)

    spop_data.append((f, update, divergences))

print "filename\tupdate\tnum_orgs\tmin_divergence\tmax_divergence\tavg_divergence\tsd"
for output in sorted(spop_data, key=lambda x: x[0]):
    fname, update, divergences = output[0], output[1], output[2]
    if len(divergences) == 0:
        continue

    print "%s\t%s\t%s\t%s\t%s\t%s\t%s" % ("\t".join([x for x in fname.split("_")]), update, len(divergences), min(divergences), max(divergences), numpy.average(divergences), numpy.std(divergences))
