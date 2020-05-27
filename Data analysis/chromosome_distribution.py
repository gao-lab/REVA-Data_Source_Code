#This script is for calculating the distribution of variants on chromosomes
import numpy as np
from scipy.stats import fisher_exact
import operator

'''BH adjusted'''
def bh_qvalues(pv):
    if pv==[]:
        return []
    m=len(pv)
    args,pv=zip(*sorted(enumerate(pv),None,operator.itemgetter(1)))
    if pv[0]<0 or pv[-1]>1:
        raise ValueError("p-value should between 0 and 1")
    qv=m*[0]
    mincoeff=pv[-1]
    qv[args[-1]]=mincoeff
    for j in xrange(m-2,-1,-1):
        coeff=m*pv[j]/float(j+1)
        if coeff<mincoeff:
            mincoeff=coeff
        qv[args[j]]=mincoeff
    return qv  

chromosome_length=np.loadtxt(open("../Data/chromosome_file.txt",'r'),delimiter="\t",dtype=np.str)
chr_number=np.loadtxt(open("../Data/chr_distribution_number.txt",'r'),delimiter="\t",dtype=np.str,skiprows=1)

chr_length_list=chromosome_length[:,2].astype(np.float)
variant_number_list=chr_number[:,3].astype(np.float) # 1-pos 2-neg 3-all

chr_length_total=np.sum(chr_length_list,axis=0)
variant_number_total=np.sum(variant_number_list,axis=0)

p_value_g_list=[]
p_value_l_list=[]

for x in range(24):
    a=variant_number_list[x]
    b=chr_length_list[x]-a
    c=variant_number_total-a
    d=chr_length_total-variant_number_total-b
    pvalue_greater=fisher_exact([[a,b],[c,d]],alternative="greater")[1]
    pvalue_less=fisher_exact([[a,b],[c,d]],alternative="less")[1]
    p_value_g_list.append(pvalue_greater)
    p_value_l_list.append(pvalue_less)

q_value_g_list=bh_qvalues(p_value_g_list)
q_value_l_list=bh_qvalues(p_value_l_list)

out=[]
out.append(["chromosome","variant number","p-value-g","FDR-g","p-value-l","FDR-l"])
for x in range(24):
    out.append([chr_number[x][0],chr_number[x][3],p_value_g_list[x],q_value_g_list[x],p_value_l_list[x],q_value_l_list[x]])
np.savetxt("all_distribution.txt",np.array(out),delimiter="\t",fmt="%s")
print("Finished.")