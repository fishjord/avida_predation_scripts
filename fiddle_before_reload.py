#!/usr/bin/python

import subprocess
import sys
import os

if len(sys.argv) != 2:
    print >>sys.stderr, "USAGE: fiddle_population.py <spop>"
    sys.exit(1)

script = os.path.join(os.path.split(sys.argv[0])[0], "sample_population.py")
cmd = [script, "high", sys.argv[1], sys.argv[1]]

subprocess.check_call(cmd)
