#!/bin/bash

set -ex

RANDOM=42

if [ $# -ne "7" ]; then
    echo "USAGE: gen_replicates.sh <sample_pop_script> <config_dir> <replicate_dir> <seed_pop> <predator_file> <num_replicates> <num_updates>"
    exit 1
fi

sample_pop=$1
config_dir=$2
run_dir=$3
seed_pop=$4
pred_file=$5
num_replicates=$6
num_updates=$7

for sgv in "clone" "intermediate" "high"
do
    if [ ! -e $run_dir/$sgv ]; then
	mkdir $run_dir/$sgv
    fi

    for sim_num in `seq 1 ${num_replicates}`
    do
	rseed=${RANDOM}
	echo "Generating $sgv sim $sim_num with rseed= $rseed"
	sim_dir=${run_dir}/$sgv/sim_$sim_num
	
	if [ -e $sim_dir ]; then
	    continue
	fi

	mkdir $sim_dir
	cp ${config_dir}/* $sim_dir/
	
	$sample_pop -r ${rseed} --predators $pred_file $sgv $seed_pop > $sim_dir/seed.spop
	
	sed -i "s/{SEED}/${RANDOM}/g" $sim_dir/avida.cfg
	sed -i "s/{UPDATES}/${num_updates}/g" $sim_dir/events-flat.cfg
    done
done