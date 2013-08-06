script_dir=/home/fishjord/cse845/scripts

phase2_dir= /mnt/scratch/fishjord/cse845_paper/phase2
predator_spop= /mnt/scratch/fishjord/cse845_paper/phase1/pred_replicates/sim_25/data/detail-2000000.spop

.PHONY: help submit_solo

help:
	$(info targets: generate_reps, solo_stats)

skel:
	ln -s /home/fishjord/cse845/scripts/skel skel

solo: skel
	$(script_dir)/solo_eval_coevopred_generation.py $(phase2_dir) $(predator_spop) . 0

solo_stats.txt:
	$(script_dir)/solo_stats_phase3.py phase3 solo/*/*/sim_* > solo_stats.txt

solo_summary.txt: solo_stats.txt
	$(script_dir)/stat_summary.py 4 solo_stats.txt > solo_summary.txt

submit_solo:
	$(script_dir)/sandbox/sub_jobs.sh 02:00:00 solo/*/*/sim_*