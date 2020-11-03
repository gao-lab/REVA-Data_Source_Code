#!/bin/bash
#-*- coding:utf-8 -*-

# Download data
rsync -aP rsync://hgdownload.cse.ucsc.edu/gbdb/hg19/multiz46way/*.wib .
rsync -aP rsync://hgdownload.cse.ucsc.edu/gbdb/hg19/multiz100way/*.wib .

wget http://hgdownload.cse.ucsc.edu/goldenpath/hg19/database/phastCons100way.txt.gz
wget http://hgdownload.cse.ucsc.edu/goldenpath/hg19/database/phyloP100wayAll.txt.gz
wget http://hgdownload.cse.ucsc.edu/goldenpath/hg19/database/phyloP46wayAll.txt.gz
wget http://hgdownload.cse.ucsc.edu/goldenpath/hg19/database/phyloP46wayPlacental.txt.gz
wget http://hgdownload.cse.ucsc.edu/goldenpath/hg19/database/phyloP46wayPrimates.txt.gz
wget http://hgdownload.cse.ucsc.edu/goldenpath/hg19/database/phastCons46way.txt.gz
wget http://hgdownload.cse.ucsc.edu/goldenpath/hg19/database/phastCons46wayPlacental.txt.gz
wget http://hgdownload.cse.ucsc.edu/goldenpath/hg19/database/phastCons46wayPrimates.txt.gz

# Prepare data for hgwiggle
gunzip *.txt.gz
ln -s *.txt *.wig
for file in `ls *.txt | cut -d '.' -f 1`
do
ln -s ${file}.txt ${file}.wig
done

# Get the conservation scores by hgwiggle
# Download hgwiggle
wget http://hgdownload.soe.ucsc.edu/admin/exe/linux.x86_64/hgWiggle
chmod +x hgWiggle

bed_file=$1 # Input variant position in bed format with GRCh37 human reference genome version
for iterm in {phastCons100way,phyloP46wayAll,phyloP46wayPrimates,phastCons46wayPlacental,phastCons46way,phastCons46wayPrimates,phyloP46wayPlacental,phyloP100wayAll}
do
{
hgWiggle -bedFile=${bed_file} ${iterm}  >> ${iterm}".txt"
}&
done
wait
