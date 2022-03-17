import mysql.connector

def connectTo(hostname, username, user_password, dbname):
    connection = None
    try:
        connection = mysql.connector.connect(
            host = hostname,
            user = username,
            passwd = user_password,
            database = dbname
        )
        print("Connected to MySQL Database: " + dbname)
    except mysql.connector.Error as err:
        print(err)

    return connection

def executeQuery(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query successful")
        return True
    except mysql.connector.Error as err:
        print(err)
        return False

def readQuery(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except mysql.connector.Error as err:
        print(err)

