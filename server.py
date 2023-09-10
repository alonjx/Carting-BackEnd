import logging
from functools import wraps
import openai
import mysql.connector
import requests
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

product_name = ""
openai.api_key = r'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'

similar_cache = {}

logging.basicConfig(level=logging.INFO)


# Function to create a database connection and cursor
def get_database_connection():
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '1234',
        'database': 'Carting_DB',
        'port': 3306
    }

    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    return connection, cursor


# Decorator to handle the database connection and cursor automatically
def with_cursor(f):
    @wraps(f)  # Use functools.wraps to preserve the original function attributes
    def wrapper(*args, **kwargs):
        connection, cursor = get_database_connection()
        try:
            # Call the actual function with the cursor as an argument
            result = f(*args, cursor=cursor, **kwargs)
        except Exception as e:
            # Properly handle any exceptions
            connection.rollback()
            raise e
        finally:
            cursor.close()
            connection.close()
        return result
    return wrapper


@app.before_request
def handle_preflight():
    if request.method == "OPTIONS":
        res = make_response()
        res.headers['X-Content-Type-Options'] = '*'
        return res


@app.route("/product/serial")
@with_cursor
def get_product_by_id(cursor):
    query_parameters = request.args
    chain_name = chains_id[query_parameters["chain_id"]]
    product_serial_number = query_parameters["product_id"]

    cursor.execute(
        f'select item_price, item_name, chain_name from product where item_code LIKE "%{product_serial_number}"'
        f'AND chain_name != "{chain_name}"')
    json_dict_result = {}

    for item in cursor.fetchall():
        res = {
            "item_price": item[0],
            "product_name": item[1],
            "chain": item[2]
        }
        json_dict_result.update(res)
    json_data = json.dumps(json_dict_result)

    cursor.close()
    return json_data


@app.route("/product/name")
def api_product_by_name():
    global product_name
    query_parameters = request.args
    product_name = query_parameters["name"]
    chain_id = query_parameters["chain_id"]
    try:
        res = get_similar_items(product_name, chain_id)
        return json.dumps(res)
    except Exception as e:
        logging.error(f'error in query: select * from product where chain_name != "{chains_id[chain_id]}"')
        logging.error(e)
        return "", 501

def is_in_stock(barcode):
    x = {"q": str(barcode), "aggs": 1, "store": "331"}
    url = 'https://www.rami-levy.co.il/api/catalog'
    response = requests.post(url, data=x)
    res = response.text
    if res:
        res = json.loads(res)
        return len(res["data"]) > 0
    else:
        return False

def cut_string_between_brackets(input_string):
    start_index = input_string.find('{')
    end_index = input_string.rfind('}')

    if start_index != -1 and end_index != -1:
        cut_string = input_string[start_index:end_index + 1]
        return cut_string
    else:
        return None


@with_cursor
def get_similar_items(product_name, chain_id, cursor):
    cache_key = f"{product_name}-{chain_id}"
    if cache_key in similar_cache:
        logging.info(f"found {cache_key} in cache")
        return similar_cache[cache_key]

    logging.warning(f"didnt find {cache_key} in cache")
    cursor.execute(f'select item_name from product where chain_name != "{chains_id[chain_id]}"')
    fetched_data = cursor.fetchall().copy()
    product_dic = {}
    for row in fetched_data:
        product_dic[row[0]] = jellyfish.jaro_similarity(row[0], product_name)
    sorted_dict = dict(sorted(product_dic.items(), key=lambda x: x[1], reverse=True)[:10])

    d = {}
    for i, v in sorted_dict.items():
        cursor.execute(f"select item_code from product where item_name='{i}'")
        fetched_data = cursor.fetchall().copy()
        if is_in_stock(fetched_data[0][0]):
            d[i] = v

    f = open('question.txt', 'r', encoding='utf-8')
    message = f.read()
    message = message.replace('<<>>', product_name)
    for key in d:
        message += f'\n{key}'
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{'role': 'system', 'content': 'You are a helpful assistant.'},
                  {'role': 'user', 'content': message}]
    )
    generated_text = response.choices[0].message.content
    print(generated_text)
    dict_text = json.loads(cut_string_between_brackets(generated_text))
    res = []
    for key in dict_text:
        temp_dict = {}
        cursor.execute(f"select item_price, item_code from product where item_name='{dict_text[key]}'")
        fetched_data = cursor.fetchall().copy()
        temp_dict['item_name'] = dict_text[key]
        temp_dict['item_price'] = fetched_data[0][0]
        temp_dict['item_code'] = fetched_data[0][1]
        res.append(temp_dict)

    res = sorted(res, key=lambda x: x['item_price'])
    logging.info(f"cache updated with key = {cache_key}")
    similar_cache[cache_key] = res
    return res
if __name__ == '__main__':
    app.run(host=host, port=port)
