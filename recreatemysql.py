import mysql.connector
import json

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="password"
)

cursor = mydb.cursor(dictionary=True)

def reimportDB():
    with open('oshes.sql', 'r') as sql_file:
        result_iterator = cursor.execute(sql_file.read(), multi=True)
        for res in result_iterator:
            print("Running query: ", res)
            if res.with_rows:
                    fetch_result = res.fetchall()
                    print(json.dumps(fetch_result, indent=4))
            elif res.rowcount > 0:
                    print(f"Affected {res.rowcount} rows" )

        mydb.commit()

############
#reimportDB()

