from recreatemysql import reimportDB
from prepopulatemysql import (
    prepopulate_all
)
import pymongo as pymgo
import json

connectMongo = pymgo.MongoClient("localhost", 27017)
db = connectMongo["assignment1"]
collectionProduct = db["products"]
collectionItem = db["items"]

with open('products.json') as file:
    file_data = json.load(file)
if isinstance(file_data, list):
    collectionProduct.insert_many(file_data)
else:
    collectionProduct.insert_one(file_data)

with open('items.json') as file:
    file_data2 = json.load(file)
if isinstance(file_data2, list):
    collectionItem.insert_many(file_data2)
else:
    collectionItem.insert_one(file_data2)

reimportDB()
prepopulate_all()