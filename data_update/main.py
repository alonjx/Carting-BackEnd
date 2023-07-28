import os
import shutil
import sql_update

from download_data import get_data_shufersal, get_data_rami_levi
from parse_data import parse_data, find_xml_path


def main():
    if os.path.exists('compressed'):
        shutil.rmtree('data')
        shutil.rmtree('compressed')
    os.mkdir('compressed')
    os.mkdir('data')
    get_data_shufersal()
    get_data_rami_levi()
    shufersal_products = parse_data(find_xml_path("413"), is_shufersal=True)
    rami_levi_products = parse_data(find_xml_path("39"), is_shufersal=False)
    sql_update.update_sql_table(shufersal_products, "shufersal")
    sql_update.update_sql_table(rami_levi_products, "rami_levi")


if __name__ == '__main__':
    main()
