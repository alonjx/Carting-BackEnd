import logging

import mysql.connector
from flask import Flask, request, make_response
import json
import jellyfish
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
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


@app.before_request
def handle_preflight():
    if request.method == "OPTIONS":
        res = make_response()
        res.headers['X-Content-Type-Options'] = '*'
        return res


@app.route("/product/serial")
def get_product_by_id():
    query_parameters = request.args
    chain_name = chains_id[query_parameters["chain_id"]]
    product_serial_number = query_parameters["product_id"]
    # TODO: maybe log?
    logging.info(f' going to execute query: select item_price, item_name, chain_name from product where item_code '
                 f'LIKE "%{product_serial_number}%" AND chain_name != "{chain_name}"')
    my_cursor.execute(
        f'select item_price, item_name, chain_name from product where item_code LIKE "%{product_serial_number}"'
        f'AND chain_name != "{chain_name}"')
    json_dict_result = {}
    for item in my_cursor.fetchall():
        res = {
            "item_price": item[0],
            "product_name": item[1],
            "chain": item[2]
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
    try:
        logging.info(f'going to execute: select * from product where chain_name != "{chains_id[chain_id]}"')
        my_cursor.execute(f'select item_name from product where chain_name != "{chains_id[chain_id]}"')
        fetched_data = my_cursor.fetchall().copy()
        product_dic = {}
        for row in fetched_data:
            if jellyfish.jaro_similarity(row[0], product_name) > 0.75:
                product_dic[row[0]] = jellyfish.jaro_similarity(row[0], product_name)
        sorted_dict = dict(sorted(product_dic.items(), key=lambda x: x[1], reverse=True))
        res = []
        i = 0
        for key in sorted_dict:
            temp_dict = {}
            if i == 3:
                break
            my_cursor.execute(f"select item_price, item_code from product where item_name='{key}'")
            fetched_data = my_cursor.fetchall().copy()
            temp_dict['item_name'] = key
            temp_dict['item_price'] = fetched_data[0][0]
            temp_dict['item_code'] = fetched_data[0][1]
            res.append(temp_dict)
            i += 1
            logging.info(f'returning: {res}')
        return json.dumps(res)
    except Exception as e:
        logging.error(f'error in query: select * from product where chain_name != "{chains_id[chain_id]}"')
        logging.error(e)
        return "", 501

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
