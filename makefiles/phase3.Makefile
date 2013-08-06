script_dir=/home/fishjord/cse845/scripts

plots: pre_phase2/solo_stats.txt post_phase2/solo_stats.txt
	Rscript $(script_dir)/R/BeforeAfterSoloPlots.R pre_phase2/solo_stats.txt post_phase2/solo_stats.txt