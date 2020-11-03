import numpy as np
from pymongo import MongoClient
from scipy import stats
import os
import sys

data_file="./data/"+sys.argv[1] #formatted variant file
accession_number=sys.argv[2] #accesion number

#convert string to number
def str2num(input_string,num_type="float"):
    if input_string!="." and input_string!="-":
        if num_type=="int":
            return int(input_string)
        else:
            return float(input_string)
    else:
        return input_string

#avoid p value 0
def adj_pvalue(p_value):
    if p_value==0:
        p_value=1e-10
        return p_value
    else:
        return p_value

def insert_to_database(data_file,accession_number):
    #connect to database
    client=MongoClient()
    db=client.emdb
    collection=db.data_experiment
    meta_collection=db.data_experiment_meta

    #Load file
    print("Loading file")
    main_temp=np.loadtxt(open(data_file,'r'),delimiter="\t",dtype=np.str,skiprows=1)
    #insert file to database
    print("Inserting data")
    fail_number=0
    for x in range(main_temp.shape[0]):
        row=main_temp[x]
        inter_id=("intid"+row[1].split("r")[1]+"_"+row[2]+"_"+row[0]+row[4]+row[5]+row[11]).lower().replace(" ","_")
        meta_id=(inter_id.replace("intid","meta")+accession_number).lower()
        annotate_id=("id"+row[1].split("r")[1]+"_"+row[0]+row[4]+row[5]).lower()
        document={"Chr":row[1],
                "Pos_37":str2num(row[2],"int"),
                "Pos_38":str2num(row[0],"int"),
                "Rs":row[3],
                "Ref":row[4],
                "Alt":row[5],
                "Start":row[6],
                "End":row[7],
                "Direction":row[8],
                "Region":row[9],
                "TF":row[10],
                "Cell_line":row[11],
                "P_value":row[12],
                "FDR":str2num(row[13]),
                "Effect":str2num(row[14]),
                "Variant_active_repress":row[15],
                "Label":row[16],
                "TF_active_repress":row[17],
                "Accession_number":accession_number,
                "Inter_id":inter_id,
                "Anno_id":annotate_id
                }
        try:
            collection.insert_one(document)
        except:
            #prepare meta document
            del document["Anno_id"]
            document["Meta_id"]=meta_id
            meta_document=document
            #find entry in main database and meta database
            result=collection.find_one({"Inter_id":inter_id})
            meta_result=meta_collection.find_one({"Meta_id":meta_id})
            #check whether new_insert is same with old_insert
            if result["Accession_number"]==accession_number:
                fail_number=fail_number+1
            elif meta_result!=None:
                fail_number=fail_number+1
            else:
                #check entry in main database is meta result or not
                if result["Accession_number"]=="reva-meta":
                    if result["Label"]=="unknown":
                        meta_collection.insert_one(meta_document)
                    elif row[12]==".":#p_value of new_insert
                        meta_collection.insert_one(meta_document)
                        collection.update_one({"Inter_id":inter_id},{'$set':{'FDR':".",'Label':"unknown"}})
                    else:
                        p_value_list=[]
                        p_value_list.append(adj_pvalue(float(row[12])))
                        meta_results=meta_collection.find({"Inter_id":inter_id})
                        for meta_result in meta_results:
                            p_value_list.append(adj_pvalue(float(meta_result["P_value"])))
                        #cal hmp and label
                        hmp_value=stats.hmean(p_value_list)
                        if hmp_value>=0.001:
                            hmp_label="0"
                        else:
                            hmp_label="1"
                        #update and insert
                        meta_collection.insert_one(meta_document)
                        collection.update_one({"Inter_id":inter_id},{'$set':{'FDR':hmp_value,'Label':hmp_label}})
                else:
                    #transfer document from main to meta database.
                    new_meta_id=(result["Inter_id"].replace("intid","meta")+result["Accession_number"]).lower()
                    del result["Anno_id"]
                    result["Meta_id"]=new_meta_id
                    if result["P_value"]=="." or row[12]==".":
                        meta_collection.insert_one(meta_document)
                        meta_collection.insert_one(result)
                        collection.update_one({"Inter_id":inter_id},{'$set':{'Start':".",
                                                                            'End':".",
                                                                            'Direction':".",
                                                                            'Region':".",
                                                                            'TF':".",
                                                                            'P_value':".",
                                                                            'FDR':".",
                                                                            'Effect':".",
                                                                            'Variant_active_repress':".",
                                                                            'Label':"unknown",
                                                                            'TF_active_repress':".",
                                                                            'Accession_number':"reva-meta"
                                                                            }})
                    else:
                        p_value_list=[]
                        p_value_list.append(adj_pvalue(float(row[12])))
                        p_value_list.append(adj_pvalue(float(result["P_value"])))
                        hmp_value=stats.hmean(p_value_list)
                        if hmp_value>=0.001:
                            hmp_label="0"
                        else:
                            hmp_label="1"
                        meta_collection.insert_one(meta_document)
                        meta_collection.insert_one(result)
                        collection.update_one({"Inter_id":inter_id},{'$set':{'Start':".",
                                                                            'End':".",
                                                                            'Direction':".",
                                                                            'Region':".",
                                                                            'TF':".",
                                                                            'P_value':".",
                                                                            'FDR':hmp_value,
                                                                            'Effect':".",
                                                                            'Variant_active_repress':".",
                                                                            'Label':hmp_label,
                                                                            'TF_active_repress':".",
                                                                            'Accession_number':"reva-meta"
                                                                            }})
    print(fail_number)

insert_to_database(data_file,accession_number)
print("Finished.")
