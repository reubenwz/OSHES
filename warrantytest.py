import json
from os import read
from mysqlaccessors import connectTo, executeQuery, readQuery
import pymongo as pymgo

connection = connectTo("localhost", "root", "password", "oshes")

connectMongo = pymgo.MongoClient("localhost", 27017)
db = connectMongo["assignment1"]
collectionProduct = db["products"]
collectionItem = db["items"]

def setOld():
    with open("warrantytestindex.txt", "r+") as f:
        line = f.readlines()[0]
        i = int(line.strip())

    CUSTOMER_ID = 1

    item = collectionItem.find({"PurchaseStatus": {"$eq": "Sold"}})[i]

    query_0 = f"SELECT COUNT(*) FROM Item WHERE itemID={item['ItemID']}"
    exists = int(readQuery(connection, query_0)[0][0]) > 0
    if not exists:
        product_id = collectionProduct.find({"Category": item["Category"], "Model": item["Model"]}, {"ProductID": 1})[0][
            'ProductID']

        query_1 = "SELECT COUNT(*) FROM Purchase"
        purchase_id = readQuery(connection, query_1)[0][0] + 1

        query_2 = "INSERT INTO Purchase VALUES ('%s','%s','%s')" % (
            purchase_id,
            "2015-10-09",
            CUSTOMER_ID
        )

        executeQuery(connection, query_2)

        # create Item
        query_3 = "INSERT INTO Item VALUES ('%s','%s','%s','%s','%s','%s','%s',%s,%s)" % (
            item['ItemID'],
            item['Color'],
            item['Factory'],
            item['PowerSupply'],
            item['ProductionYear'],
            item['Model'],
            item['ServiceStatus'],
            product_id,
            purchase_id
        )

        executeQuery(connection, query_3)

        collectionItem.find_one_and_update(
            {"ItemID": item['ItemID']}, {"$set": {"PurchaseStatus": "Sold"}}
        )

        print("Successful Execution")

    else:
        print("Unsuccessful Execution, Try Again")

    with open('warrantytestindex.txt', 'w+') as f:
            f.write(f"{i + 1}")