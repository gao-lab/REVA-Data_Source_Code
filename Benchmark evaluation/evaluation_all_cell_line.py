#This script is for evaluation of all invloved tools except EnsembleExpr.
#This script is also for the evaluation on different cell lines.
import os
import numpy as np
from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_curve
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import auc

def cal_core(tool_name,label_name,cutoff,true_label,pred_label):
    true_label=true_label.astype(np.float64)
    pred_label=pred_label.astype(np.float64)
    pred_label_adj=np.where(pred_label>cutoff,1,0)


    total_number=true_label.shape[0]
    pos_number=int(sum(true_label)[0])
    print total_number,pos_number
    roc_score=roc_auc_score(true_label,pred_label)

    precision,recall, thresholds = precision_recall_curve(true_label,pred_label)
    auprc=auc(recall,precision)

    TP=float(np.sum(np.logical_and(np.equal(true_label,1),np.equal(pred_label_adj,1))))
    TN=float(np.sum(np.logical_and(np.equal(true_label,0),np.equal(pred_label_adj,0))))
    FP=float(np.sum(np.logical_and(np.equal(true_label,0),np.equal(pred_label_adj,1))))
    FN=float(np.sum(np.logical_and(np.equal(true_label,1),np.equal(pred_label_adj,0))))
    
    sensitivity= TP/(TP + FN)
    specificity= TN/(TN + FP)
    if TP+FP==0:
        precision="N.A."
    else:
        precision= TP/(TP+FP)
    FDR= FP/(TN+FP)
    if TP==0:
        F1score="N.A."
    else:
        F1score= (2*precision*sensitivity)/(precision+sensitivity)
    accuracy= (sensitivity+specificity)/2
    out=[tool_name,label_name,total_number,pos_number,TP,TN,FP,FN,sensitivity,
                specificity,precision,FDR,F1score,accuracy,roc_score,auprc] 
    return out


def cal_result(file="../Data/benchmark_multi_label.txt"):
    result_file="./result/benchmark_result.txt"
    target_path="./"
    
    target_file=target_path+file
    print("Load %s ..." % file)
    temp=np.loadtxt(open(target_file,'r'),delimiter="\t",dtype=np.str,skiprows=1)
    predict_score=temp[:,13:]
    true_label=temp[:,5:6]
    
    print("Cal all result...")
    result_out=[]
    tool_list=["CADD","DeepSEA","Eigen","Eigen-PC","ExPecto","FunSeq2","GWAVA-Region","GWAVA-TSS","GWAVA-Unmatch"]
    cutoff_list=[10,0.99,5,9,0.3,2,0.5,0.5,0.5]
    
    for x in range(len(tool_list)):
        temp_out=cal_core(tool_list[x],"All_Label",cutoff_list[x],true_label,predict_score[:,x:x+1])
        result_out.append(temp_out)
    
    # deal with cell line result
    print("deal cell line label...")
    cell_line_list=["GM18507_Label","HEK293T_Label","HepG2_Label","K562_Label","K562_GATA1_Label","NA12878&NA19239_label","SH-SY5H_label"]
    
    tp1=[]
    tp2=[]
    tp3=[]
    tp4=[]
    tp5=[]
    tp6=[]
    tp7=[]

    for x in range(temp.shape[0]):
        if temp[x][6]!="NA":
            tp1.append(temp[x])
        if temp[x][7]!="NA":
            tp2.append(temp[x])
        if temp[x][8]!="NA":
            tp3.append(temp[x])
        if temp[x][9]!="NA":
            tp4.append(temp[x])
        if temp[x][10]!="NA":
            tp5.append(temp[x])
        if temp[x][11]!="NA":
            tp6.append(temp[x])
        if temp[x][12]!="NA":
            tp7.append(temp[x])
    
    tp1=np.array(tp1)
    tp2=np.array(tp2)
    tp3=np.array(tp3)
    tp4=np.array(tp4)
    tp5=np.array(tp5)
    tp6=np.array(tp6)
    tp7=np.array(tp7)

    tp=[tp1,tp2,tp3,tp4,tp5,tp6,tp7]
    for x in range(len(cell_line_list)):
        print("Deal with %s " % cell_line_list[x])
        for y in range(len(tool_list)):
            temp_out=cal_core(tool_list[y],cell_line_list[x],cutoff_list[y],tp[x][:,6+x:7+x],tp[x][:,13+y:14+y])
            result_out.append(temp_out)
    
    result_out=np.array(result_out)
    np.savetxt(result_file,result_out,delimiter="\t",fmt="%s")
    print("Finished.")
    
cal_result()

        

    



