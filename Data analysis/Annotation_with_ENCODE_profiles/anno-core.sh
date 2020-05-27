#!/bin/bash
#This is the core annotation script.

echo $1
#make dict
mkdir ./temp/$1
cp ./temp/temp1.file /./temp/$1/temp1.file 
cd ./temp/$1
#find overlap with anno
bedtools intersect -a temp1.file -b ./all_bed_without_cell_line/$1.bed -wa | sort | uniq > temp2.file
#find overlap without anno
cat temp1.file temp2.file | sort | uniq -u > temp3.file
#add pos label
awk '{printf "1\n"}' temp2.file > pos.label
paste -d "\t" temp2.file pos.label >pos.result
#add neg label
awk '{printf "0\n"}' temp3.file > neg.label
paste -d "\t" temp3.file neg.label >neg.result
#merge pos and neg result, sort
cat pos.result neg.result | sort -t $'\t' -k1 -k2 -k4 -k5 -k6 >file.result
#add feature title
echo $1 > feature.title
#cut file
cut -f 8 file.result > feature.result
cat feature.title feature.result > ../anno_tmp/$1
rm -rf ./temp/$1