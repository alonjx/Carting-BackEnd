import gzip
import shutil
import xml.etree.ElementTree as ET
from product import Product
import os


def parse_data(xml_path, is_shufersal):
    data = []

    tree = ET.parse(xml_path)
    root = tree.findall('Items/Item')

    if is_shufersal:
        for item in root:
            data.append(Product(item.find('PriceUpdateDate').text, item.find('ItemCode').text, item.find('ItemType').text,
                        item.find('ItemName').text, item.find('ManufacturerName').text, item.find('ManufactureCountry').text,
                        item.find('ManufacturerItemDescription').text, item.find('UnitQty').text, item.find('Quantity').text,
                        item.find('bIsWeighted').text, item.find('UnitOfMeasure').text, item.find('QtyInPackage').text,
                        item.find('ItemPrice').text, item.find('UnitOfMeasurePrice').text, item.find('AllowDiscount').text,
                        item.find('ItemStatus').text))
    else:
        for item in root:
            data.append(Product(item.find('PriceUpdateDate').text, item.find('ItemCode').text, item.find('ItemType').text,
                        item.find('ItemNm').text, item.find('ManufacturerName').text, item.find('ManufactureCountry').text,
                        item.find('ManufacturerItemDescription').text, item.find('UnitQty').text, item.find('Quantity').text,
                        item.find('bIsWeighted').text, item.find('UnitOfMeasure').text, item.find('QtyInPackage').text,
                        item.find('ItemPrice').text, item.find('UnitOfMeasurePrice').text, item.find('AllowDiscount').text,
                        item.find('ItemStatus').text))

    for dat in data:
        print(dat.item_name)


def find_shufersal_xml_path():
    for filename in os.listdir(os.getcwd() + '\\data'):
        file_path = 'data\\' + filename
        tree = ET.parse(file_path)
        root = tree.findall('StoreId')
        if root[0].text == '413':
            return file_path
    return None


def find_rami_levi_xml_path():
    for filename in os.listdir(os.getcwd() + '\\data'):
        file_path = 'data\\' + filename
        tree = ET.parse(file_path)
        root = tree.findall('StoreId')
        if root[0].text == '39':
            return file_path
    return None
