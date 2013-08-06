script_dir= /home/fishjord/cse845/scripts
phase1_dir= /mnt/scratch/fishjord/cse845_paper/phase1/

nopred_dir= $(phase1_dir)/nopred_replicates
pred_dir= $(phase1_dir)/pred_replicates

final_update=data/detail-2000000.spop

nopred_seed_rep= $(nopred_dir)/sim_21/$(final_update)
pred_seed_rep= $(pred_dir)/sim_30/$(final_update)
predators= $(pred_dir)/sim_14/$(final_update)

.PHONY: plots

skel:
	ln -s $(script_dir)/skel/phase2 skel

pred_replicates: skel
	mkdir pred_replicates
	$(script_dir)/phase2_replicate_generation.sh $(script_dir)/sample_population.py skel pred_replicates $(pred_seed_rep) $(predators) 30 200000

nopred_replicates: skel
	mkdir nopred_replicates
	$(script_dir)/phase2_replicate_generation.sh $(script_dir)/sample_population.py skel nopred_replicates $(nopred_seed_rep) $(predators) 30 200000

sub_replicates: pred_replicates nopred_replicates
	$(script_dir)/sandbox/sub_jobs.sh 48:00:00 */*/sim_*

solo_stats.txt:
	$(script_dir)/solo_stats_phase2.py phase2 */*/sim_* > solo_stats.txt || (rm solo_stats.txt && false)

shannon_diversity.txt:
	$(script_dir)/shannon_diversity.py */*/sim_*/data/detail-*.spop > shannon_diversity.txt

plots: solo_stats.txt shannon_diversity.txt
	Rscript $(script_dir)/R/phase2_plots.R solo_stats.txt shannon_diversity.txt
