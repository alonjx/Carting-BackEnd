-- create database Carting_DB;
use Carting_DB;
CREATE TABLE product (
    chain_name VARCHAR(50),
	price_update_date VARCHAR(50),
    item_code VARCHAR(50),
    item_name varchar(200),
    manufacturer_item_description varchar(100),
    unity_qty varchar(50),
    quantity integer,
    unit_of_measure varchar(50),
    qty_in_package float,
    item_price float,
    unit_of_measure_price float,
    item_status varchar(10),
    PRIMARY KEY (item_code, chain_name)
)
DEFAULT CHARACTER SET utf8
COLLATE utf8_general_ci;