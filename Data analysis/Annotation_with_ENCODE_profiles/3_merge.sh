#!/bin/bash

#go into target dict and copy file for merging
cd ./result/$1
cp file.info temp.info

#merge features
for line in $(cat ./ref_file/feature_list_without_cell_line.txt);do
    feature=$line
    paste -d "\t" temp.info $feature > temp
    rm -rf temp.info
    mv temp temp.info
done
mv temp.info ../result_merge/$1
echo "Finished."
    