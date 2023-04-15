import mysql.connector
import psycopg2

import product

def update_sql_table(products, chain_name):
  mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="2nik",
    database="Carting_DB",
    port=3306
  )
  mycursor = mydb.cursor()
  for single_product in products:
    if "\'" in single_product.item_name:
      single_product.item_name = single_product.item_name.replace("\'", "")
    try:
      line_to_exec = f"Insert into product (item_name, item_code) values ('{single_product.item_name}', '{single_product.item_code}');"
      mycursor.execute(line_to_exec)
    except mysql.connector.Error as error:
      print(f"Failed to insert record into MySQL table: {error}")

  mydb.commit()
  mycursor.execute("select * from product")

  rows = mycursor.fetchall()
  for row in rows:
    print(row)
  mycursor.close()
  mydb.close()