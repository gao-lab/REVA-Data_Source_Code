import numpy as np
from pymongo import MongoClient
import os

#function for inserting accession information into database
def insert_accession_info(file):
    #open file
    accession_file="./accession/"+file
    sup_temp=np.loadtxt(open(accession_file,'r'),delimiter="\n",dtype=np.str)
    #connect to database
    client=MongoClient()
    db=client.emdb
    accession_collection=db.data_experiment_info
    accession_info={"Accession_number":sup_temp[0],
                "Created_time":sup_temp[1],
                "Updated_time":sup_temp[2],
                "Method_category":sup_temp[3],
                "Method_detail":sup_temp[4],
                "Raw_data":sup_temp[5],
                "Species":sup_temp[6],
                "Reference_genome_version":sup_temp[7],
                "Cutoff":sup_temp[8],
                "Literature":sup_temp[9],
                "Doi":sup_temp[10]
                }
    accession_collection.insert_one(accession_info)
    print("Finish %s" % file)

for file_name in os.listdir("./accession"):
    insert_accession_info(file_name)
print("Finish All.")