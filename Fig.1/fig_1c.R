library(karyoploteR)

#Read positive data
vars <- read.table("../Data/positive_variants.txt", comment.char = "", header = TRUE)
vars <- toGRanges(vars[,c(1,3,3,3:length(vars))])
seqlevelsStyle(vars) <- "UCSC"

svg(file="./pics/fig_1c_pos.svg")
#Plot positive variants as density
kp <- plotKaryotype(genome="hg19")
kpPlotDensity(kp, data=vars)
dev.off()

#Read negative data
vars <- read.table("../Data/negative_variants.txt", comment.char = "", header = TRUE)
vars <- toGRanges(vars[,c(1,3,3,3:length(vars))])
seqlevelsStyle(vars) <- "UCSC"

svg(file="./pics/fig_1c_neg.svg")
#Plot negative variants as density
kp <- plotKaryotype(genome="hg19")
kpPlotDensity(kp, data=vars)
dev.off()