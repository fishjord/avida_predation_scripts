script_dir= /home/fishjord/cse845/scripts

.PHONY: plots selected_plots

skel:
	ln -s /home/fishjord/cse845/scripts/skel skel

pred_replicates: skel
	mkdir pred_replicates
	$(script_dir)/phase1_replicate_generation.sh skel/phase1_pred pred_replicates 30 2000000

nopred_replicates: skel
	mkdir nopred_replicates
	$(script_dir)/phase1_replicate_generation.sh skel/phase1_nopred nopred_replicates 30 2000000

sub_pred_replicates: pred_replicates
	$(script_dir)/sandbox/sub_jobs.sh 120:00:00,feature=intel10 pred_replicates/sim_* 

sub_nopred_replicates: nopred_replicates
	$(script_dir)/sandbox/sub_jobs.sh 108:00:00,feature=intel10 nopred_replicates/sim_*

solo_stats.txt:
	$(script_dir)/solo_stats_phase1.py */sim_* > solo_stats.txt || (rm solo_stats.txt && false)

shannon_diversity.txt:
	$(script_dir)/shannon_diversity.py */sim_*/data/detail-*.spop > shannon_diversity.txt

plots: solo_stats.txt shannon_diversity.txt
	cd plots && Rscript $(script_dir)/R/phase1_plots.R ../solo_stats.txt ../shannon_diversity.txt

selected_solo_stats.txt:
	$(script_dir)/solo_stats_phase1.py nopred_replicates/sim_21 pred_replicates/sim_30 > selected_solo_stats.txt || (rm selected_solo_stats.txt && false)

selected_shannon_diversity.txt:
	$(script_dir)/shannon_diversity.py nopred_replicates/sim_21/data/detail-*.spop pred_replicates/sim_30/data/detail-*.spop > selected_shannon_diversity.txt

selected_plots: selected_solo_stats.txt selected_shannon_diversity.txt
	cd selected_plots && Rscript $(script_dir)/R/phase1_plots.R ../selected_solo_stats.txt ../selected_shannon_diversity.txt
