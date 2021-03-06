# coding=utf-8
#operation involve mongodb will be placed here
from string import Template
import os
# ---MongoDB
import pymongo
from pymongo import MongoClient

url = "mongodb://$dbuser:$dbpassword@ds021346.mlab.com:21346/chiahaya"
mongo_us = 'Ankabot'
mongo_ps = os.environ['MONGO_PSW']
temp=Template(url)
mongo_url=temp.substitute(dbuser=mongo_us,dbpassword=mongo_ps)
client = MongoClient(mongo_url)
db = client['chiahaya']

def insert_data(Collection,dict):
    op_ins=db[Collection]
    op_ins.insert_one(dict)
    return

def get_doc(Collection,pipeline):
    op_ins=db[Collection]
    ins=op_ins.find(pipeline)
    if ins is None:
        return None
    else:
        result=[]
        for i in ins:
            result.append(i)
        return result
            
def modify_doc(Collection,pipeline,key,value):
    op_ins=db[Collection]

    ins=op_ins.find_one(pipeline)
    if ins is not None:
        op_ins.update_one(pipeline,
        {'$set':{key:value}})
    else:
        dict=pipeline
        pipeline[key]=value
        op_ins.insert_one(dict)