#!/bin/bash --login

set -e
base=`pwd`

run_sim=$(cd `dirname $0` &>/dev/null; pwd; cd - &>/dev/null)/run_sim.sh

walltime=$1
shift

for sim_dir in $*
do
    echo "Submitting $sim_dir"
    cd $base/$sim_dir
    sim_dir_abspath=`pwd`

    if [ ! -e avida.cfg ]; then
	echo "  No avida.cfg, skipping"
	continue
    fi

    if [ -e submitted ]; then
	echo "Already submitted, skipping"
	continue
    fi

    qsub -l mem=3000mb,walltime=${walltime} -j oe -m abe -N `basename $sim_dir` -v sim_dir=$sim_dir_abspath $run_sim
    touch submitted
done

cd $base