import re

import mysql.connector
from flask import Flask, request
import json
import jellyfish


app = Flask(__name__)
host = "localhost"
port = 8080
chains_id = {'1': 'rami_levi',
             '2': 'shufersal'}

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="2nik",
    database="Carting_DB",
    port=3306
)
my_cursor = mydb.cursor()

product_name = ""

@app.route("/product/serial")
def get_product_by_id():
    query_parameters = request.args
    chain_name = chains_id[query_parameters["chain_id"]]
    product_serial_number = query_parameters["product_id"]
    # TODO: maybe log?
    # print(f'select item_price, chain_name from product where item_code = "{chain_name} " '
    #                   f'AND chain_name != "{product_serial_number}"')
    my_cursor.execute(f'select item_price, chain_name from product where item_code = "{product_serial_number}" '
                      f'AND chain_name != "{chain_name}"')
    json_dict_result = {}
    for item in my_cursor.fetchall():
        res = {
            "item_price": item[0],
            "chain": item[1]
        }
        json_dict_result.update(res)
    json_data = json.dumps(json_dict_result)
    return json_data


@app.route("/product/name")
def get_similar_items():
    global product_name
    query_parameters = request.args
    product_name = query_parameters["name"]
    chain_id = query_parameters["chain_id"]
    my_cursor.execute(f'select * from product where chain_name != "{chains_id[chain_id]}"')
    fetched_data = my_cursor.fetchall().copy()
    product_dic = {}
    for row in fetched_data:
        if jellyfish.jaro_similarity(row[3], product_name) > 0.75:
            product_dic[row[3]] = jellyfish.jaro_similarity(row[3], product_name)

    sorted_dict = dict(sorted(product_dic.items(), key=lambda x: x[1], reverse=True))
    res = {}
    i = 0
    for key in sorted_dict:
        if i == 3:
            break
        my_cursor.execute(f"select item_price from product where item_name='{key}'")
        fetched_data = my_cursor.fetchall().copy()
        res[key] = fetched_data[0][0]
        i += 1
    print(res)

    return json.dumps(res)
    # if " " not in product_name:
    #     for row in fetched_data:
    #         tokens = word_tokenize(row[3])
    #         if product_name in tokens:
    #             print(tokens)
    #
    # else:
    #     test_dic = {}
    #     for row in fetched_data:
    #         if jellyfish.jaro_similarity(row[3], product_name) > 0.75:
    #             print(jellyfish.jaro_similarity(row[3], product_name), "->", row[3])
    #             test_dic[row[3]] = jellyfish.jaro_similarity(row[3], product_name)
    #
    #     sorted_dict = dict(sorted(test_dic.items(), key=lambda x: x[1], reverse=True))
    #     for key in sorted_dict:
    #         print(key, "->", sorted_dict[key])
    #


if __name__ == '__main__':
    app.run(host=host, port=port)