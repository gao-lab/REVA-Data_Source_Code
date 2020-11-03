import numpy as np
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'

'''Read file contains reference and alternative sequences'''
def read_file(path):
    sequence_info = open(path, 'r')
    temp_file=np.loadtxt(sequence_info,delimiter="\t",dtype=np.str,skiprows=1)
    temp_ref=temp_file[:,0]
    temp_alt=temp_file[:,1]
    sequence_info.close()
    return temp_ref,temp_alt  

'''One-hot coding'''
def code(seq, target, order):
    for i in range(len(seq)):
        if((seq[i]=="A")|(seq[i]=='a')):
            target[order,i,0]=1
        if((seq[i]=='C')|(seq[i]=='c')):
            target[order,i,1]=1
        if((seq[i]=='G')|(seq[i]=='g')):
            target[order,i,2]=1
        if((seq[i]=='T')|(seq[i]=='t')):
            target[order,i,3]=1

def conversion_seq(temp):
    seq_length=sequence_len
    seq_num=len(temp)
    #onehot coding
    seq_code = np.zeros((seq_num, seq_length, 4), dtype=np.int)
    for j in range(seq_num):
        sequence = temp[j][0]
        code(sequence, seq_code, j)
    print seq_code.shape    
    return seq_code
 
def onehot(path):
    temp_ref,temp_alt=read_file(path)
    data=[conversion_seq(temp_ref),conversion_seq(temp_alt)]
    print("Finish one-hot-encoding.")
    return data

'''prediction'''
def prediction(model, data):
    predicted = model.predict(data, batch_size=128, verbose=2)
    return predicted

'''get para file from feature name'''
def feature2para():
    model_para_list=os.listdir(model_para_prefix)
    p_dict={}
    for para in model_para_list:
        feature=para.split("_")[0]
        p_dict[feature]=para
    return p_dict

'''function for calculating fold_change'''
def cal_fold_change(ref_out,alt_out):
    pos_label=np.ones(ref_out.shape, dtype=np.float)*(1+1e-8)
    out=np.log2(ref_out/(pos_label-ref_out))-np.log2(alt_out/(pos_label-alt_out))
    return out

'''load model with feature id'''
para_dict=feature2para()
def get_model(feature_id):
    file_load=para_dict[feature_id]
    fn=int(file_load.split("_")[4])
    fl=int(file_load.split("_")[5])
    pl=int(file_load.split("_")[6])
    un=int(file_load.split("_")[7])
    model=cnn_model(filter_num=fn,filter_len=fl,pool_len=pl,units=un)
    model.load_weights(model_para_file)
    return model
