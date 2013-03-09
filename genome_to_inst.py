#!/usr/bin/python

import sys
import avida_utils

if len(sys.argv) != 3:
    print >>sys.stderr, "USAGE: genome_to_inst.py <instset_file> <genome_string>"
    sys.exit(1)

inst_set = avida_utils.read_inst(sys.argv[1])
for c in sys.argv[2]:
    op = avida_utils.get_op(c)
    print inst_set[op], op, avida_utils.get_symbol(op), c
