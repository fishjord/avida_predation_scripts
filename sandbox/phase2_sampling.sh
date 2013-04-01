#!/bin/bash

set -ex

sample_script=/home/fishjord/documents/cse845/project/scripts/sample_population.py
seed=42
base_dir=/home/fishjord/documents/cse845/project/phase2

#sim_2m_6     1199    199     1842.71356784 avg look instructions
predators_spop=/home/fishjord/documents/cse845/project/phase1/pred/sim_2m_6/data/detail-2000000.spop
nopred_prey_spop=/home/fishjord/documents/cse845/project/phase1/nopred/sim_6/data/detail-2000000.spop
pred_prey_spop=/home/fishjord/documents/cse845/project/phase1/pred/sim_2m_29/data/detail-2000000.spop

#clone_nopred_phase2  clone_pred_phase2  do_sampling.sh  do_sampling.sh~  high_nopred_phase2  high_pred_phase2  intermediate_nopred_phase2  intermediate_pred_phase2

$sample_script -r $seed --predators $predators_spop high $pred_prey_spop > ${base_dir}/high_pred_phase2/conf/seed.spop
$sample_script -r $seed --predators $predators_spop high $nopred_prey_spop > ${base_dir}/high_nopred_phase2/conf/seed.spop
$sample_script -r $seed --predators $predators_spop clone $pred_prey_spop > ${base_dir}/clone_pred_phase2/conf/seed.spop
$sample_script -r $seed --predators $predators_spop clone $nopred_prey_spop > ${base_dir}/clone_nopred_phase2/conf/seed.spop
$sample_script -r $seed --predators $predators_spop --replicates 55 intermediate $pred_prey_spop > ${base_dir}/intermediate_pred_phase2/conf/seed.spop
$sample_script -r $seed --predators $predators_spop --replicates 55 intermediate $nopred_prey_spop > ${base_dir}/intermediate_nopred_phase2/conf/seed.spop

