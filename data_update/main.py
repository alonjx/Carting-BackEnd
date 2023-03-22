import os
import shutil

from download_data import  get_data_shufersal, get_data_rami_levi
from parse_data import parse_data, find_xml_path



if __name__ == '__main__':
    if os.path.exists('compressed'):
        shutil.rmtree('data')
        shutil.rmtree('compressed')
    os.mkdir('compressed')
    os.mkdir('data')
    get_data_shufersal()
    get_data_rami_levi()
    parse_data(find_xml_path(413), is_shufersal=True)
    parse_data(find_xml_path(39), is_shufersal=False)

