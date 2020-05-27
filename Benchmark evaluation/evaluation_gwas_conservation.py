#This script is for evaluation on variants with different conservation score or whether involved in GWAS catalog.
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
    b_accuracy= (sensitivity+specificity)/2
    out=[tool_name,label_name,total_number,pos_number,TP,TN,FP,FN,sensitivity,
                specificity,precision,FDR,F1score,b_accuracy,roc_score,auprc]
    return out

def cal_by_conv(temp,result_file,tool_list,cutoff_list):
    print("class by conv_score...")
    result_out=[]
    Convs_list=["Convs_0_0.2","Convs_0.2_0.4","Convs_0.4_0.6","Convs_0.6_0.8","Convs_0.8_1.0"]
    
    tp1=[]
    tp2=[]
    tp3=[]
    tp4=[]
    tp5=[]

    for x in range(temp.shape[0]):
        conv_score=float(temp[x][6]) #phastCons100way
        if conv_score<0.2:
            tp1.append(temp[x])
        elif 0.4>conv_score>=0.2:
            tp2.append(temp[x])
        elif 0.6>conv_score>=0.4:
            tp3.append(temp[x])
        elif 0.8>conv_score>=0.6:
            tp4.append(temp[x])
        else:
            tp5.append(temp[x])
   
    tp1=np.array(tp1)
    tp2=np.array(tp2)
    tp3=np.array(tp3)
    tp4=np.array(tp4)
    tp5=np.array(tp5)

    tp=[tp1,tp2,tp3,tp4,tp5]
    for x in range(len(Convs_list)):
        print("Deal with %s " % Convs_list[x])
        for y in range(len(tool_list)):
            temp_out=cal_core(tool_list[y],Convs_list[x],cutoff_list[y],tp[x][:,5:6],tp[x][:,15+y:16+y])
            result_out.append(temp_out)
    
    result_out=np.array(result_out)
    np.savetxt(result_file,result_out,delimiter="\t",fmt="%s")
    print("Finished.")

def cal_by_gwas(temp,result_file,tool_list,cutoff_list):
    print("class by gwas_label...")
    result_out=[]
    gwas_list=["gwas_0","gwas_1"]
    
    tp1=[]
    tp2=[]

    for x in range(temp.shape[0]):
        gwas_label=float(temp[x][14]) #gwas_label
        if gwas_label==0:
            tp1.append(temp[x])
        else:
            tp2.append(temp[x])
   
    tp1=np.array(tp1)
    tp2=np.array(tp2)

    tp=[tp1,tp2]
    for x in range(len(gwas_list)):
        print("Deal with %s " % gwas_list[x])
        for y in range(len(tool_list)):
            temp_out=cal_core(tool_list[y],gwas_list[x],cutoff_list[y],tp[x][:,5:6],tp[x][:,15+y:16+y])
            result_out.append(temp_out)
    
    result_out=np.array(result_out)
    np.savetxt(result_file,result_out,delimiter="\t",fmt="%s")
    print("Finished.")    

def cal_result(file="../Data/benchmark_conservation_gwas.txt"):
    result_file="./results/benchmark_result_gwas.txt"
    target_path="./"
    
    target_file=target_path+file
    print("Load %s ..." % file)
    temp=np.loadtxt(open(target_file,'r'),delimiter="\t",dtype=np.str,skiprows=1)
    
    tool_list=["CADD","CARMEN","DeepSEA","Eigen","Eigen-PC","ExPecto","FunSeq2","GWAVA-Region","GWAVA-TSS","GWAVA-Unmatch"]
    cutoff_list=[10,0.005,0.99,5,9,0.3,2,0.5,0.5,0.5]
    # class by conv_score
    #cal_by_conv(temp,result_file,tool_list,cutoff_list)
    # class by gwas_label
    cal_by_gwas(temp,result_file,tool_list,cutoff_list)
    
cal_result()

        

    



