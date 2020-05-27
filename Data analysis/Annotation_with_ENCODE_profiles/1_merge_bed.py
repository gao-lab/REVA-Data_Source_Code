import os
import shutil
import time
import subprocess

cate="acc" #acc, his, tf, met
envir='bedtools'
bed_path="../data_"+cate+"/bed_without_cell_line/"
temp_path="../temp/"
merge_target=open("../ref_file/repeat_"+cate+"_without_cell_line.txt",'r')


def merger(file1,file2):
    print file1,file2
    
    outfile=temp_path+"tmp1.bed"
    output=temp_path+"tmp.bed"
    cmd="cat %s %s | sort -k1,1 -k2,2n > %s" % (file1,file2,outfile)
    subprocess.call(cmd,shell=True)
    
    if os.path.exists(temp_path+"tmp.bed"):
        os.remove(temp_path+"tmp.bed")
    cmd='%s merge -i %s > %s' % (envir,outfile,output)
    subprocess.call(cmd,shell=True)
    os.remove(outfile)
    

t0 = time.time()
print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
for line in merge_target.readlines():
    temp=[]
    temp=line.split("\t")
    temp.pop()
    print "Merging files ", " ".join(temp)
    for x in range(len(temp)):
        if x==0:
            try:
                merger(bed_path+temp[x]+".bed",bed_path+temp[x+1]+".bed")
                os.remove(bed_path+temp[x]+".bed")
                os.remove(bed_path+temp[x+1]+".bed")
            except:
                pass
        elif (len(temp)-x)>1:
            try:
                merger(temp_path+"tmp.bed",bed_path+temp[x+1]+".bed")
                os.remove(bed_path+temp[x+1]+".bed")
            except:
                pass
        else:
            break
    try:        
        os.rename(temp_path+"tmp.bed",temp_path+temp[0]+".bed")
        shutil.move(temp_path+temp[0]+".bed",bed_path+temp[0]+".bed")
    except:
        pass

    
t1 = time.time()
print("Merging took %f hours" % ((t1-t0)/3600))
print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())