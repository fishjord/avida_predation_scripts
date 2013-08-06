#!/bin/bash

set -ex

RANDOM=42

if [ $# -ne "4" ]; then
    echo "USAGE: gen_replicates.sh <config_dir> <replicate_dir> <num_replicates> <num_updates>"
    exit 1
fi

config_dir=$1
run_dir=$2
num_replicates=$3
num_updates=$4

if [ ! -e $run_dir ]; then
    mkdir $run_dir
fi

for sim_num in `seq 1 ${num_replicates}`
do
    sim_dir=${run_dir}/sim_$sim_num
    
    if [ -e $sim_dir ]; then
	continue
    fi
    
    mkdir $sim_dir
    cp ${config_dir}/* $sim_dir/
    
    sed -i "s/{SEED}/${RANDOM}/g" $sim_dir/avida.cfg
    sed -i "s/{UPDATES}/${num_updates}/g" $sim_dir/events-flat.cfg
done