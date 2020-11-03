import numpy as np
from pymongo import MongoClient

def prepare_doc(title_list,row):
    document={}
    for x in range(len(title_list)):
        document[title_list[x]]=row[x]
    return document

def insert_gene_disease(file_path):
    client=MongoClient()
    db=client.emdb
    collection=db.disease_variant
    temp=np.loadtxt(open(file_path,'r'),dtype=np.str,delimiter='\t')
    title=temp[0]
    content=temp[1:,]
    print content.shape
    i=0
    for x in range(content.shape[0]):
        row=content[x]
        document=prepare_doc(title,row)
        try:
            collection.insert_one(document)
        except:
            i=i+1
    print("Insert data successfully.")
    print("Failing in insert %s data." % i)

insert_gene_disease(disgenet_file)