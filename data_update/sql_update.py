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
    if "\'" in single_product.item_name or "\\" in single_product.item_name:
        single_product.item_name = single_product.item_name.replace("\'", "")
        single_product.item_name = single_product.item_name.replace("\\", "")

    if "\'" in single_product.unity_qty or "\\" in single_product.unity_qty:
        single_product.unity_qty = single_product.unity_qty.replace("\'", "")
        single_product.unity_qty = single_product.unity_qty.replace("\\", "")

    if single_product.manufacturer_item_description is not None and "\'" in single_product.manufacturer_item_description\
            or "\\" in single_product.manufacturer_item_description:
        single_product.manufacturer_item_description = single_product.manufacturer_item_description.replace("\'", "")
        single_product.manufacturer_item_description = single_product.manufacturer_item_description.replace("\\", "")

    if single_product.quantity is not None and "\'" in single_product.quantity:
        single_product.quantity = single_product.quantity.replace("\'", "")

    if single_product.unit_of_measure is not None and "\'" in single_product.unit_of_measure:
        single_product.unit_of_measure = single_product.unit_of_measure.replace("\'", "")


    try:
        line_to_exec = f"Insert into product (chain_name, price_update_date, item_code, item_name," \
                     f"manufacturer_item_description, unity_qty, quantity," \
                     f" unit_of_measure, qty_in_package, item_price, unit_of_measure_price, item_status )" \
                     f" values ('{chain_name}', '{single_product.price_update_date}', '{single_product.item_code}'," \
                     f"'{single_product.item_name}', " \
                     f"'{single_product.manufacturer_item_description}', '{single_product.unity_qty}', " \
                     f"'{single_product.quantity}', '{single_product.unit_of_measure}', " \
                     f"'{single_product.qty_in_package}', '{single_product.item_price}', '{single_product.unit_of_measure_price}', " \
                     f"'{single_product.item_status}')"
        mycursor.execute(line_to_exec)
    except mysql.connector.Error as error:
        print(error)
        print(f"Insert into product (chain_name, price_update_date, item_code, item_name," \
                     f"manufacturer_item_description, unity_qty, quantity," \
                     f" unit_of_measure, qty_in_package, item_price, unit_of_measure_price, item_status )" \
                     f" values ('{chain_name}', '{single_product.price_update_date}', '{single_product.item_code}'," \
                     f"'{single_product.item_name}', " \
                     f"'{single_product.manufacturer_item_description}', '{single_product.unity_qty}', " \
                     f"'{single_product.quantity}', '{single_product.unit_of_measure}', " \
                     f"'{single_product.qty_in_package}', '{single_product.item_price}', '{single_product.unit_of_measure_price}', " \
                     f"'{single_product.item_status}')")

  mydb.commit()
  #mycursor.execute("select * from product")

  rows = mycursor.fetchall()
  for row in rows:
    print(row)
  mycursor.close()
  mydb.close()