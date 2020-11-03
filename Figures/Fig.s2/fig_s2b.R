library('reshape2')
library('ggplot2')
library(stringr)
library(ggpubr)

infile <- read.table("../../Data/cnn_average_annotations.txt",sep='\t',stringsAsFactors = F, header = T)
colnames(infile) <- c("Feature Category","Positive","Negative")
infilep <-melt(infile) 
colnames(infilep) <- c("Feature Category","Variant Class","Average Number of Annotation")
infilep$`Feature Category` <- factor(infilep$`Feature Category`,levels = c("DNA Accessibility","Transcription Factor","Histone Modification","DNA Methylation"))

#============================Wilcox test==============================================
sta_result <- wilcox.test(infile$Positive,infile$Negative,alternative = "greater")
sta_result$p.value
#============================Make plot================================================

ggplot(infilep, aes(`Feature Category`, `Average Number of Annotation`, fill=factor(`Variant Class`)))+
  geom_boxplot()+
  stat_compare_means(label = "p.signif",aes(group = `Variant Class`),label.y = 1.03 )+
  theme_bw()+
  theme(panel.grid.major=element_blank(),panel.grid.minor=element_blank())+
  scale_y_continuous(limits = c(0.0,1.03),breaks=seq(0.0, 1, 0.1))+
  theme(axis.text.y=element_text(size = 7,color = "black"))+
  theme(axis.text.x=element_text(size = 7,color = "black"))+
  theme(axis.title.x = element_text(size = 7))+
  theme(axis.title.y = element_text(size = 7))+
  guides(fill = guide_legend(title = ""))+
  theme(panel.border= element_blank())+
  theme(axis.line= element_line(size=0.5, colour ="black"))+
  theme(legend.position="top")+
  theme(legend.text=element_text(size=7))+
  coord_cartesian(ylim = c(0.0, 1.05))+
  scale_x_discrete(labels = function(x) str_wrap(x, width = 15))


ggsave("./fig_s2b.png", width = 15, height = 15, units = "cm")
