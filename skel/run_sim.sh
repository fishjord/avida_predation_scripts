#!/bin/bash --login
# Time job will take to execute (HH:MM:SS format)
#PBS -l walltime=114:00:00
# Memory needed by the job
#PBS -l mem=250mb
# Make output and error files the same file
#PBS -j oe
# Send an email when a job is aborted, begins or ends
#PBS -m abe
# Give the job a name
#PBS -N avida_pred_sim
# Request a job array

#qsub -l mem=3000mb,walltime=168:00:00 -j oe -o /mnt/scratch/fishjord/cse845_avida/preditor_sim/${i}_gridout.txt -m abe -N avida_pred_sim_${i} /mnt/home/fishjord/cse845/run_pred_sim.sh

if [ -z $sim_num ]; then
    echo "sim_num must be set"
    exit 1
fi

if [ -z $num_updates ]; then
    echo "num_updates must be set"
    exit 1
fi

if [ -z $run_dir ]; then
    echo "run_dir must be set"
    exit 1
fi

avida=${run_dir}/avida
skeleton_dir=${run_dir}/conf/
wd=${run_dir}
sim_dir=${wd}/sim_$sim_num

mkdir $sim_dir
cd $sim_dir
cp ${skeleton_dir}/* ./

sed -i "s/{SEED}/${RANDOM}/g" avida.cfg
sed -i "s/{UPDATES}/${num_updates}/g" events-flat.cfg

$avida &> avida_log.txt