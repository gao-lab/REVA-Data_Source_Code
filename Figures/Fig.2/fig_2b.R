library(karyoploteR)

#Read positive data
pos_bars <- read.table("../../Data/positive_variants.txt", comment.char = "", header = TRUE)
neg_vars <- read.table("../../Data/negative_variants.txt", comment.char = "", header = TRUE)

#Build a GRanges and convert chromosome names from "1" to "chr1" 
pos_bars <- toGRanges(pos_bars[,c(1,3,3,3:length(pos_bars))])
neg_vars <- toGRanges(neg_vars[,c(1,3,3,3:length(neg_vars))])
seqlevelsStyle(pos_bars) <- "UCSC"
seqlevelsStyle(neg_vars) <- "UCSC"

svg(file="./fig_2b.svg")
#Plot SNPs as density
kp <- plotKaryotype(genome="hg19")
kpPlotDensity(kp, data=pos_bars, r0=0.6, r1=1.0, col="#FF6633")
kpPlotDensity(kp, data=neg_vars, r0=0.1, r1=0.5, col="#6699CC")
dev.off()