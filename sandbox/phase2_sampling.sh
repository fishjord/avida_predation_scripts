#!/bin/bash

set -ex

sample_script=/home/fishjord/cse845/scripts/sample_population.py
seed=42
base_dir=.

#sim_2m_6     1199    199     1842.71356784 avg look instructions
predators_spop=/home/fishjord/cse845/paper_replicates/phase1/predator_sim/sim_2m_6/data/detail-2000000.spop
nopred_prey_spop=/home/fishjord/cse845/paper_replicates/phase1/nopred_sims/sim_9/data/detail-2000000.spop
pred_prey_spop=/home/fishjord/cse845/paper_replicates/phase1/predator_sim/sim_2m_29/data/detail-2000000.spop

#clone_nopred_phase2  clone_pred_phase2  do_sampling.sh  do_sampling.sh~  high_nopred_phase2  high_pred_phase2  intermediate_nopred_phase2  intermediate_pred_phase2

for sgv in clone intermediate high
do
    for hist in pred nopred
    do
	mkdir -p ${base_dir}/${hist}/${sgv}
	cp -r conf ${base_dir}/${hist}/${sgv}/
	cp ${base_dir}/run_sim.sh ${base_dir}/${hist}/${sgv}/
    done
done

$sample_script -r $seed --predators $predators_spop high $pred_prey_spop > ${base_dir}/pred/high/conf/seed.spop
$sample_script -r $seed --predators $predators_spop high $nopred_prey_spop > ${base_dir}/nopred/high/conf/seed.spop
$sample_script -r $seed --predators $predators_spop clone $pred_prey_spop > ${base_dir}/pred/clone/conf/seed.spop
$sample_script -r $seed --predators $predators_spop clone $nopred_prey_spop > ${base_dir}/nopred/clone/conf/seed.spop
$sample_script -r $seed --predators $predators_spop --replicates 55 intermediate $pred_prey_spop > ${base_dir}/pred/intermediate/conf/seed.spop
$sample_script -r $seed --predators $predators_spop --replicates 55 intermediate $nopred_prey_spop > ${base_dir}/nopred/intermediate/conf/seed.spop

