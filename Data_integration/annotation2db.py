import numpy as np
from pymongo import MongoClient
import sys
csv_file_path=sys.argv[1]
anno_file_path=sys.argv[2]

def insert_new_data(csv_file_path,anno_file_path):
    client=MongoClient()
    db=client.emdb
    collection=db.data_experiment_anno
    temp=np.loadtxt(open(csv_file_path),dtype=np.str,delimiter=',')
    annotation=np.loadtxt(open(anno_file_path),dtype=np.str,delimiter='\t')
    if annotation.shape==(2431,):
        annotation=annotation.reshape(1,2431)
    i=0
    if temp.shape==(11,):
        temp=temp.reshape(1,11)
    for x in range(temp.shape[0]):
        row=temp[x]
        id_38=("id"+row[0].split('r')[1]+"_"+row[2]+row[4]+row[5]).lower()       
        id_19=("id"+row[0].split('r')[1]+"_"+row[1]+row[4]+row[5]).lower()
        anno=annotation[x][6:]
        document={"Chr":row[0],
                  "Pos_37":int(row[1]),
                  "Pos_38":int(row[2]),
                  "Rs":row[3],
                  "Ref":row[4],
                  "Alt":row[5],
                  "Id_38":id_38,
                  "Id_19":id_19,
                  "Annotation":anno.tolist()
                 }
        try:
            collection.insert_one(document)
        except:
            i=i+1
    print("Insert data successfully.")
    print("%s data exist in database already." % i)

#insert data to database
insert_new_data(csv_file_path,anno_file_path)