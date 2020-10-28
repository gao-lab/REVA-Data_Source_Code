import os
import numpy as np
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_curve
from sklearn.metrics import auc

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def cal_auc(true_label,pred_label):
    true_label=true_label.astype(np.float64)
    pred_label=pred_label.astype(np.float64)
    print("Cal...")
    fpr,tpr,thresholds_auc=roc_curve(true_label,pred_label)
    roc_score=roc_auc_score(true_label,pred_label)
    #precision,recall, thresholds_prc = precision_recall_curve(true_label,pred_label)
    #auprc=auc(recall,precision)
    return fpr,tpr,roc_score

tool_list=["CADD","DeepSEA","Eigen","Eigen-PC","ExPecto","FunSeq2","GWAVA-Region","GWAVA-TSS","GWAVA-Unmatch"]
color_list=["#DC143C","#0000FF","#008000","#FF00FF","#00BFFF","#90EE90","#8A2BE2","#4169E1","#FFA500","#696969"]

#load file
print("Loading files...")
all_file=np.loadtxt(open("../Data/benchmark_multi_label.txt",'r'),delimiter="\t",dtype=np.str,skiprows=1)
ensemble_file=np.loadtxt(open("../Data/benchmark_EnsembleExpr_5_merge.txt",'r'),delimiter="\t",dtype=np.str)
#get result
result=[]
#cal emsemble result
fpr,tpr,auroc=cal_auc(ensemble_file[:,5:6],ensemble_file[:,6:7])
result.append([fpr,tpr,auroc,"EnsembleExpr"])
# cal other result
for x in range(len(tool_list)):
    fpr,tpr,auroc=cal_auc(all_file[:,5:6],all_file[:,13+x:14+x])
    result.append([fpr,tpr,auroc,tool_list[x]])

#sort by auc
def take3rd(elem):
    return elem[2]
result.sort(key=take3rd,reverse=True)

#draw picture
plt.figure(dpi=300)
lw = 1.5
for x in range(len(color_list)):
    plt.plot(result[x][0], result[x][1],
         label=result[x][3]+' (AUC = {0:0.3f})'
               ''.format(result[x][2]),
         color=color_list[x],lw=lw)
        
plt.plot([0, 1], [0, 1], color='red', lw=2, linestyle='--')
plt.xlim([0.0, 1.05])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver operating characteristic')
plt.legend(loc="lower right",fontsize=8)
plt.savefig("./pics/fig_2b.png")
print("Finished.")