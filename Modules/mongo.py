import os
import pymongo
from pymongo import MongoClient
from Models.models import FileInfo, Certificate


connectionString = os.getenv("Connection_String")
appinfo = MongoClient(connectionString)

db = appinfo["appinfo"]
collection = db["appinfo"]


#insert data into the database
async def insert_data(data: dict):
    collection.insert_one(data)


#get data from the database
async def get_data(data: dict):
    return collection.find_one(data)


# get top 10 most recently updated documents
async def get_top_10_recently_updated():
    result = collection.find().sort([('_id', pymongo.DESCENDING)]).limit(10)
    data = []
    for document in result:
        data.append(document)
    return data


