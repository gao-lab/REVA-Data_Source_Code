import os
import gzip
import multiprocessing

raw_data_path="./data_acc/raw/" #data_acc, data_tf, data_his, data_met
target_path=raw_data_path.replace("raw","bed_without_cell_line")

def get_bed(file):
    file_name=(file.split("/")[-1]).split(".")[0]+".bed"
    f_bed=open(target_path+file_name,'w')
    chr_list=['chr1','chr2','chr3','chr4','chr5','chr6','chr7','chr8','chr9','chr10',
    'chr11','chr12','chr13','chr14','chr15','chr16','chr17','chr18','chr19','chr20','chr21',
    'chr22','chrX','chrY']
    
    with gzip.open(file,'rt') as pf:
        for line in pf:
            if line.split("\t")[0] in chr_list:
                f_bed.write(line.split("\t")[0]+"\t"+line.split("\t")[1]+"\t"+line.split("\t")[2]+"\n")
    f_bed.close()
    print("%s done" %file_name)

pool = multiprocessing.Pool(processes = 8)
file_list=os.listdir(raw_data_path)    
for file in file_list:
    file=raw_data_path+file
    pool.apply_async(get_bed,(file,))
pool.close()
pool.join()
print("Finished")