import download_data
import parse_data



if __name__ == '__main__':
    download_data.get_data_shufersal()
    download_data.get_data_rami_levi()
    parse_data.parse_data()
