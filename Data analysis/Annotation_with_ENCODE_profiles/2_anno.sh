#!/bin/bash

#get raw file

mkdir ./temp
mkdir ./anno_tmp/
cat $1 | awk '{printf "%s\t%s\t%s\t%s\t%s\t%s\t%s\n" ,$1,$2,$3,$4,$5,$6,$7}' >temp/temp1.file
cd temp
cat temp1.file | sort -t $'\t' -k1 -k2 -k4 -k5 -k6 >file.info
echo -e "Chr\tPos\tPos\tRef\tAlt\tLabel\tLocus" > file.title
cat file.title file.info > ../anno_tmp/file.info

i=0
for line in $(cat ./ref_file/feature_list_without_cell_line.txt);do
    feature_list[$i]=$line
    i=$i+1
done

parallel -j 16 bash ./anno-core.sh ::: ${feature_list[*]} &
wait

rm -rf ./temp
mv ./anno_tmp ./result/$1



