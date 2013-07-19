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
summary(BA.data)

#BA.data$before_after <- factor (BA.data$before_after, levels(BA.data$before_after)[c(2,1)])


lastupdate <- subset(BA.data, BA.data$update == "9000")

summary(lastupdate)


#Subset the data into predator absent and present (pabs, ppres)

high <- subset(lastupdate, lastupdate$init_diversity == "high")
high.pabs <- subset(high, high$treatment == "PredatorAbsent")
high.ppres <- subset(high, high$treatment == "PredatorPresent")

intermediate <- subset(lastupdate, lastupdate$init_diversity == "intermediate")
intermediate.pabs <- subset(intermediate, intermediate$treatment == "PredatorAbsent")
intermediate.ppres <- subset(intermediate, intermediate$treatment == "PredatorPresent")

clone <- subset(lastupdate, lastupdate$init_diversity == "clone")
clone.pabs <- subset(clone, clone$treatment == "PredatorAbsent")
clone.ppres <- subset(clone, clone$treatment == "PredatorPresent")

ConfInt <- function(y){
	
  mean_x <- mean(y)
  std_dev_x <- sd(y)
  std_err_x <- sd(y) / sqrt(length(y))
  
  lower_CI_x <- mean_x + std_err_x * (qt(p = 0.05 / 2, df = length(y) - 1))
  upper_CI_x <- mean_x + std_err_x * (qt(p = (1 - 0.05 / 2), df = length(y) - 1))
	
  return(c(lower_CI_x, upper_CI_x))
}


#####
#Plot
#6 figures for each of moves, rotations, and looks
#####

pdf("move_plots.pdf")
par(mfrow = c(2,3), mar = c(0,1,1,0), oma = c(5,4,2,4), family = "serif", cex.axis = 1.5)

#Plot moves

with(clone.ppres, lineplot.CI(x.factor = before_after, response = moves, group = pred_history, ci.fun = function(y) ConfInt(y), x.leg = 0.95, y.leg=0.0001, xlab = "", cex = 1.5, cex.leg = 1.5, cex.axis = 1.5, xaxt = 'n'))
mtext("Clone", side = 3, cex = 1, line = 0.15)
mtext("Prey moves / total prey instructions", side = 2, cex = 1.2, line = 2, outer = T)
text(2.05, 0.05, "A", cex = 2, pch = c(1,16,15))

with(intermediate.ppres, lineplot.CI(x.factor = before_after, response = moves, group = pred_history, ci.fun = function(y) ConfInt(y), legend = F, xlab = "", ylab = "", yaxt = 'n', cex = 1.5, cex.axis = 1.5, xaxt = 'n'))
mtext("Intermediate", side = 3, cex = 1, line = 0.15)
text(2.05, 0.05, "B", cex = 2, pch = c(1,16,15))

with(high.ppres, lineplot.CI(x.factor = before_after, response = moves, group = pred_history, ci.fun = function(y) ConfInt(y), legend = F, xlab = "", cex = 1.5, ylab = "", yaxt = 'n', cex.axis = 1.5, xaxt = 'n'))
mtext("High", side = 3, cex = 1, line = 0.15)
text(2.05, 0.05,  "C", cex = 2, pch = c(1,16,15))

mtext("Predator Present", side = 4, cex = 1.2, line = 1.5)

#Plot moves

with(clone.pabs, lineplot.CI(x.factor = before_after, response = moves, group = pred_history, ci.fun = function(y) ConfInt(y), x.leg = 1, xlab = "", cex = 1.5, legend = F, cex.axis = 1.5))
text(2.05, 0.05, "D", cex = 2, pch = c(1,16,15))

with(intermediate.pabs, lineplot.CI(x.factor = before_after, response = moves, group = pred_history, ci.fun = function(y) ConfInt(y), legend = F, xlab = "", ylab = "", yaxt = 'n', cex = 1.5, cex.axis = 1.5))
text(2.05, 0.05, "E", cex = 2, pch = c(1,16,15))

with(high.pabs, lineplot.CI(x.factor = before_after, response = moves, group = pred_history, ci.fun = function(y) ConfInt(y), legend = F, xlab = "", cex = 1.5, ylab = "", yaxt = 'n', cex.axis = 1.5))
mtext("Predator Absent", side = 4, cex = 1.2, line = 1.5)
mtext("Before or After Phase 2", side = 1, cex = 1.2, outer = T, line = 3)
text(2.05, 0.05, "F", cex = 2, pch = c(1,16,15))

dev.off()

###Same plot style as moves but with rotates
pdf("rotate_plots.pdf")
par(mfrow = c(2,3), mar = c(1,1,1.2,0), oma = c(5,4,2,4), family = "serif", cex.axis = 1.5)

#Plot turns

with(clone.ppres, lineplot.CI(x.factor = before_after, response = rotate, group = pred_history, ci.fun = function(y) ConfInt(y), x.leg = 0.95, y.leg = 0.00002, xlab = "", cex = 1.5, cex.leg = 1.5, cex.axis = 1.5, xaxt = 'n'))
mtext("Clone", side = 3, cex = 1, line = 0.15)
mtext("Prey turns / total prey instructions", side = 2, cex = 1.2, line = 2, outer = T)
text(2.05, 0.05, "A", cex = 2, pch = c(1,16,15))

with(intermediate.ppres, lineplot.CI(x.factor = before_after, response = rotate, group = pred_history, ci.fun = function(y) ConfInt(y), legend = F, xlab = "", ylab = "", yaxt = 'n', cex = 1.5, cex.axis = 1.5, xaxt = 'n'))
mtext("Intermediate", side = 3, cex = 1, line = 0.15)
text(2.05, 0.05, "B", cex = 2, pch = c(1,16,15))

with(high.ppres, lineplot.CI(x.factor = before_after, response = rotate, group = pred_history, ci.fun = function(y) ConfInt(y), legend = F, xlab = "", cex = 1.5, ylab = "", yaxt = 'n', cex.axis = 1.5, xaxt = 'n'))
mtext("High", side = 3, cex = 1, line = 0.15)
text(2.05, 0.05,  "C", cex = 2, pch = c(1,16,15))

mtext("Predator Present", side = 4, cex = 1.2, line = 1.5)

#Plot turns

with(clone.pabs, lineplot.CI(x.factor = before_after, response = rotate, group = pred_history, ci.fun = function(y) ConfInt(y), x.leg = 1, xlab = "", cex = 1.5, legend = F, cex.axis = 1.5))
text(2.05, 0.05, "D", cex = 2, pch = c(1,16,15))

with(intermediate.pabs, lineplot.CI(x.factor = before_after, response = rotate, group = pred_history, ci.fun = function(y) ConfInt(y), legend = F, xlab = "", ylab = "", yaxt = 'n', cex = 1.5, cex.axis = 1.5))
text(2.05, 0.05, "E", cex = 2, pch = c(1,16,15))

with(high.pabs, lineplot.CI(x.factor = before_after, response = rotate, group = pred_history, ci.fun = function(y) ConfInt(y), legend = F, xlab = "", cex = 1.5, ylab = "", yaxt = 'n', cex.axis = 1.5))
mtext("Predator Absent", side = 4, cex = 1.2, line = 1.5)
mtext("Before or After Phase 2", side = 1, cex = 1.2, outer = T, line = 3)
text(2.05, 0.05, "F", cex = 2, pch = c(1,16,15))
dev.off()

###Same plot style as moves and rotates but with looks
pdf("look_plots.pdf")
par(mfrow = c(2,3), mar = c(1,1,1,0), oma = c(5,4,2,4), family = "serif")

#Plot looks

with(clone.ppres, lineplot.CI(x.factor = before_after, response = looks, group = pred_history, ci.fun = function(y) ConfInt(y), x.leg = 0.9, y.leg = 0.00005, xlab = "", cex = 1.5, cex.leg = 1.5, cex.axis = 1.5, xaxt = 'n'))
mtext("Clone", side = 3, cex = 1, line = 0.15)
mtext("Prey looks / total prey instructions", side = 2, cex = 1.2, line = 2, outer = T)
text(2.05, 0.95, "A", cex = 2, pch = c(1,16,15))

with(intermediate.ppres, lineplot.CI(x.factor = before_after, response = looks, group = pred_history, ci.fun = function(y) ConfInt(y), legend = F, xlab = "", ylab = "", yaxt = 'n', cex = 1.5, cex.axis = 1.5, xaxt = 'n'))
mtext("Intermediate", side = 3, cex = 1, line = 0.15)
text(2.05, 0.95, "B", cex = 2, pch = c(1,16,15))

with(high.ppres, lineplot.CI(x.factor = before_after, response = looks, group = pred_history, ci.fun = function(y) ConfInt(y), legend = F, xlab = "", cex = 1.5, ylab = "", yaxt = 'n', cex.axis = 1.5, xaxt = 'n'))
mtext("High", side = 3, cex = 1, line = 0.15)
text(2.05, 0.95,  "C", cex = 2, pch = c(1,16,15))

mtext("Predator Present", side = 4, cex = 1.2, line = 1.5)

#Plot looks

with(clone.pabs, lineplot.CI(x.factor = before_after, response = looks, group = pred_history, ci.fun = function(y) ConfInt(y), x.leg = 1, xlab = "", cex = 1.5, legend = F, cex.axis = 1.5))
text(2.05, 0.95, "D", cex = 2, pch = c(1,16,15))

with(intermediate.pabs, lineplot.CI(x.factor = before_after, response = looks, group = pred_history, ci.fun = function(y) ConfInt(y), legend = F, xlab = "", ylab = "", yaxt = 'n', cex = 1.5, cex.axis = 1.5))
text(2.05, 0.95, "E", cex = 2, pch = c(1,16,15))

with(high.pabs, lineplot.CI(x.factor = before_after, response = looks, group = pred_history, ci.fun = function(y) ConfInt(y), legend = F, xlab = "", cex = 1.5, ylab = "", yaxt = 'n', cex.axis = 1.5))
mtext("Predator Absent", side = 4, cex = 1.2, line = 1.5)
mtext("Before or After Phase 2", side = 1, cex = 1.2, outer = T, line = 3)
text(2.05, 0.95, "F", cex = 2, pch = c(1,16,15))
dev.off()



pdf("attack_plots.pdf")
par(mfrow = c(1,3), mar = c(1,1,1,0), oma = c(4,4,2,4), family = "serif")

#Plot pred attacks

with(clone.ppres, lineplot.CI(x.factor = before_after, response = pred_attacks, group = pred_history, ci.fun = function(y) ConfInt(y), x.leg = 0.95, xlab = "", cex = 1.5, cex.leg = 1.5, cex.axis = 1.5, xaxt = 'n', y.leg = 1000000))
mtext("Clone", side = 3, cex = 1, line = 0.15)
mtext("Predator Attacks", side = 2, cex = 1.2, line = 2.4, outer = T)
#text(2.05, 900000, "A", cex = 2, pch = c(1,16,15))

mtext("before", side = 1, cex = 1, line = 0.7, adj = 0.05)
mtext("after", side = 1, cex = 1, line = 0.7, adj = 0.955)

with(intermediate.ppres, lineplot.CI(x.factor = before_after, response = pred_attacks, group = pred_history, ci.fun = function(y) ConfInt(y), legend = F, xlab = "", ylab = "", yaxt = 'n', cex = 1.5, cex.axis = 1.5, xaxt = 'n'))
mtext("Intermediate", side = 3, cex = 1, line = 0.15)
#text(2.05, 900000, "B", cex = 2, pch = c(1,16,15))

mtext("before", side = 1, cex = 1, line = 0.7, adj = 0.05)
mtext("after", side = 1, cex = 1, line = 0.7, adj = 0.955)

with(high.ppres, lineplot.CI(x.factor = before_after, response = pred_attacks, group = pred_history, ci.fun = function(y) ConfInt(y), legend = F, xlab = "", cex = 1.5, ylab = "", yaxt = 'n', cex.axis = 1.5, xaxt = 'n'))
mtext("High", side = 3, cex = 1, line = 0.15)
#text(2.05, 900000, "C", cex = 2, pch = c(1,16,15))

mtext("Before or After Phase 2", side = 1, cex = 1.2, outer = T, line = 2.1, )
mtext("before", side = 1, cex = 1, line = 0.7, adj = 0.05)
mtext("after", side = 1, cex = 1, line = 0.7, adj = 0.955)

dev.off()