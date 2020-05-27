library(VariantAnnotation)
library(TxDb.Hsapiens.UCSC.hg19.knownGene) # for annotation
library(org.Hs.eg.db)                      # to convert from Entrez Gene ID to Symbol

input <- data.frame(read.table('../Data/positive_variants.txt',header = F,sep = '\t'))
colnames(input) <- c('chr','pos_s','pos_e','ref','alt','info')
input$pos_s <- as.numeric(as.character(input$pos_s))
input$pos_e <- as.numeric(as.character(input$pos_e))
target <- with(input,
               GRanges( seqnames = Rle(chr),
                        ranges = IRanges(pos_s, end=pos_e, names=info),
                        strand = Rle(strand("*")) ) )

library(TxDb.Hsapiens.UCSC.hg19.knownGene)
loc <- locateVariants(target, TxDb.Hsapiens.UCSC.hg19.knownGene, AllVariants())
names(loc) <- NULL
out <- as.data.frame(loc)
out$names <- names(target)[ out$QUERYID ]
out$label <- input$label[ out$QUERYID ]
out <- out[ , c("names", "seqnames", "start", "end", "LOCATION")]
out <- unique(out)
write.table(out,file = "./positive_locus_annotation.txt",col.names = F,row.names = F,sep = '\t',quote = F)

