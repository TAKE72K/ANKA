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