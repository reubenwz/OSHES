import json
from mysqlaccessors import connectTo, executeQuery, readQuery

connection = connectTo("localhost", "root", "password", "oshes")

def prepopulate_product(data):
    for row in data:
        product_id = row['ProductID']
        category = row['Category']
        model = row['Model']
        cost = row['Cost ($)']
        price = row['Price ($)']
        warranty = row['Warranty (months)']

        query_string = f"INSERT INTO Product VALUES({product_id},'{category}','{model}',{cost},{price},{warranty})"
        executeQuery(connection, query_string)
    print('success!')

def prepopulate_user(data):
    for row in data: 
        customer_id = row['CustomerID']
        name = row['Name']
        gender = row['Gender']
        email_address = row['EmailAddress']
        phone_number = row['PhoneNumber']
        address = row['Address']
        password = row['Password']
        query_string = f"INSERT INTO Customer VALUES({customer_id}, \
            '{name}','{gender}','{email_address}','{phone_number}','{address}', '{password}')"
        executeQuery(connection, query_string)
    print('success!')

        
def prepopulate_admin(data):
    for row in data: 
        admin_id = row['AdminID']
        name = row['Name']
        gender = row['Gender']
        phone_number = row['PhoneNumber']
        password = row['Password']
        query_string = f"INSERT INTO Administrator VALUES({admin_id}, \
            '{name}','{gender}','{phone_number}','{password}')"
        executeQuery(connection, query_string)
    print('success!')

def prepopulate_all():
    try:
        with open("products.json", encoding="utf-8") as f:
            data = json.loads(f.read())
            prepopulate_product(data)

        with open("customers.json", encoding="utf-8") as f:
            data = json.loads(f.read())
            prepopulate_user(data)
        
        with open("administrators.json", encoding="utf-8") as f:
            data = json.loads(f.read())
            prepopulate_admin(data)

    except FileNotFoundError:
        print("Err! File does not exist")
        
