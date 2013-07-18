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

avida=/mnt/scratch/fishjord/cse845_paper/avida

cd $sim_dir

if $avida &> avida_log.txt; then
    touch completed
else
    touch failed
fi