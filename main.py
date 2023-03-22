import os
import shutil

import download_data
import parse_data



if __name__ == '__main__':
    if os.path.exists('compressed'):
        shutil.rmtree('data')
        shutil.rmtree('compressed')
    os.mkdir('compressed')
    os.mkdir('data')
    download_data.get_data_shufersal()
    download_data.get_data_rami_levi()
    parse_data.parse_data(parse_data.find_shufersal_xml_path(), True)
    parse_data.parse_data(parse_data.find_rami_levi_xml_path(), False)

