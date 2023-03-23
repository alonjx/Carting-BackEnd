import mysql.connector
import product

def update_sql_table(products, chain_name):
  mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="2nik",
    database="testDB"
  )
  mycursor = mydb.cursor()
  mycursor.execute("select *from persons")

  for table in mycursor.description:
    print(table)



if __name__ == '__main__':
    update_sql_table(None, None)