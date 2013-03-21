#!/bin/bash --login

num_replicates=1
updates=1000
wd=$(cd `dirname $0` &>/dev/null; pwd; cd - &>/dev/null)

echo "Submitting $num_replicates replicates of $update update simulations with working directory $wd"

for i in `seq $num_replicates`
do
    qsub -l mem=3000mb,walltime=168:00:00 -j oe -m abe -N avida_${updates}_sims -v sim_num=${updates}_${i},num_updates=${updates},run_dir=${wd} ${wd}/run_sim.sh
done
