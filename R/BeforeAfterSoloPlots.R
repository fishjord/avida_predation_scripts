args <- commandArgs(trailingOnly = TRUE)

if (length(args) != 2) {
   stop("USAGE: BeforeAfterSoloPlots.R <pre_eval> <post_eval>")
}

library(sciplot)
library(lme4)

pre <- read.table(args[1], header=T)
post <- read.table(args[2], header=T)

pre$before_after = as.factor(rep("before", nrow(pre)))
post$before_after = as.factor(rep("after", nrow(pre)))
summary(pre)
summary(post)
BA.data = rbind(pre, post)
BA.data["ratio_moves"] <- BA.data["moves"] / (BA.data["prey_insts"] + .0001)
BA.data["ratio_looks"] <- BA.data["looks"] / (BA.data["prey_insts"] + .0001)
BA.data["ratio_rotate"] <- BA.data["rotate"] / (BA.data["prey_insts"] + .0001)
summary(BA.data)

#BA.data$before_after <- factor (BA.data$before_after, levels(BA.data$before_after)[c(2,1)])

BA.data <- subset(BA.data, BA.data$update == "10000")

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

   for(treatment in c("PredatorPresent", "PredatorAbsent")) {
      for(sgv in c("clone", "intermediate", "high")) {
         ss = data[data$init_diversity %in% sgv & data$treatment %in% treatment, ]
   	 with(ss, lineplot.CI(x.factor = get(fact), response = get(resp), group = get(group), ci.fun = function(y) ConfInt(y), x.leg = 0.95, y.leg=0.0001, cex = 1.5, cex.leg = 1.5, cex.axis = 1.5, ylim=ylim, xaxt = 'n'))
	 mtext(sgv, side = 3, cex = 1, line = 0.15)
	 mtext(resp, side = 2, cex = 1.2, line = 2, outer = T)
	 #text(2.05, 0.05, "A", cex = 2, pch = c(1,16,15))
      }
      mtext(treatment, side = 4, cex = 1.2, line = 1.5)
   }

   mtext("Before or After Phase 2", side = 1, cex = 1.2, outer = T, line = 2.1, )
   mtext("before", side = 1, cex = 1, line = 0.7, adj = 0.05)
   mtext("after", side = 1, cex = 1, line = 0.7, adj = 0.955)   
   dev.off()
}

do.plot(BA.data, "before_after", "num_prey", "pred_history")
do.plot(BA.data, "before_after", "moves", "pred_history")
do.plot(BA.data, "before_after", "looks", "pred_history")
do.plot(BA.data, "before_after", "rotate", "pred_history")
do.plot(BA.data, "before_after", "ratio_moves", "pred_history")
do.plot(BA.data, "before_after", "ratio_looks", "pred_history")
do.plot(BA.data, "before_after", "ratio_rotate", "pred_history")
do.plot(BA.data, "before_after", "prey_insts", "pred_history")
do.plot(BA.data, "before_after", "num_pred", "pred_history")
do.plot(BA.data, "before_after", "pred_attacks", "pred_history")
