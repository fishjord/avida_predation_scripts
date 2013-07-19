args <- commandArgs(trailingOnly = TRUE)

if (length(args) != 2) {
   stop("USAGE: phase2_plots.R <solo_stats.txt> <shannon_diversity.txt")
}

library(sciplot)
library(lme4)

BA.data <- read.table(args[1], header=T)
summary(BA.data)

updates = seq(0, 200000, 10000)

BA.data <- BA.data[BA.data$update %in% updates, ]

summary(BA.data)

ConfInt <- function(y){
	
  mean_x <- mean(y)
  std_dev_x <- sd(y)
  std_err_x <- sd(y) / sqrt(length(y))
  
  lower_CI_x <- mean_x + std_err_x * (qt(p = 0.05 / 2, df = length(y) - 1))
  upper_CI_x <- mean_x + std_err_x * (qt(p = (1 - 0.05 / 2), df = length(y) - 1))
	
  return(c(lower_CI_x, upper_CI_x))
}

do.plot <- function(data, fact, resp, group) {
   pdf(paste(resp, "plots.pdf", sep="_"))
   par(mfrow = c(2,3), mar = c(0,1,1,0), oma = c(5,4,2,4), family = "serif", cex.axis = 1.5)
   r = with(data, get(resp))

   ylim = c(min(r) * .90, max(r) * 1.1)

   for(hist_conting in c("PredatorPresent", "PredatorAbsent")) {
      for(sgv in c("clone", "intermediate", "high")) {
         ss = data[data$init_diversity %in% sgv & data$pred_history %in% hist_conting, ]
   	 with(ss, lineplot.CI(x.factor = get(fact), response = get(resp), group = get(group), ci.fun = function(y) ConfInt(y), x.leg = 0.95, y.leg=0.0001, cex = 1.5, cex.leg = 1.5, cex.axis = 1.5, ylim=ylim, xaxt = 'n'))
	 mtext(sgv, side = 3, cex = 1, line = 0.15)
	 mtext(resp, side = 2, cex = 1.2, line = 2, outer = T)
	 #text(2.05, 0.05, "A", cex = 2, pch = c(1,16,15))
      }
      mtext(hist_conting, side = 4, cex = 1.2, line = 1.5)
   }
   
   dev.off()
}

#####
#Plot
#6 figures for each of moves, rotations, and looks
#####

do.plot(BA.data, "update", "num_prey", "pred_history")
do.plot(BA.data, "update", "moves", "pred_history")
do.plot(BA.data, "update", "looks", "pred_history")
do.plot(BA.data, "update", "rotate", "pred_history")
do.plot(BA.data, "update", "prey_insts", "pred_history")
do.plot(BA.data, "update", "num_pred", "pred_history")
do.plot(BA.data, "update", "pred_attacks", "pred_history")

## Shannon diversity


div.data <- read.table(args[2], header=T)
do.plot(div.data, "update", "shannon_diversity", "init_diversity")
