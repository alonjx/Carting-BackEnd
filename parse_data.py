import gzip
import shutil
import xml.etree.ElementTree as ET
from product import Product



def parse_data():
    data = []

    tree = ET.parse('data/PriceFull7290027600007-413-202303110340.xml')
    root = tree.findall('Items/Item')

    for item in root:
        data.append(Product(item.find('PriceUpdateDate').text, item.find('ItemCode').text, item.find('ItemType').text,
                    item.find('ItemName').text, item.find('ManufacturerName').text, item.find('ManufactureCountry').text,
                    item.find('ManufacturerItemDescription').text, item.find('UnitQty').text, item.find('Quantity').text,
                    item.find('bIsWeighted').text, item.find('UnitOfMeasure').text, item.find('QtyInPackage').text,
                    item.find('ItemPrice').text, item.find('UnitOfMeasurePrice').text, item.find('AllowDiscount').text,
                    item.find('ItemStatus').text))

    for dat in data:
        print(dat.item_name)

