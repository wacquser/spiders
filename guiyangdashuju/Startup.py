#-*- coding: UTF-8 -*-

import FirstTry
import Redownload

class Startup(object):
    def __init__(self,config_file,record_file):
        first_try = FirstTry.Download(config_file, record_file)
        first_try.config_logging()
        if first_try.record_file_exists(record_file):
            redownload = Redownload.ReDownload(record_file)
        else:
            orders = first_try.parse_config_file(config_file)

            orders_after_download_ent_list = first_try.download_enterprise_list(orders)
            first_try.write_to_json_file(record_file, orders_after_download_ent_list)

            orders_after_download_ent_info = first_try.download_ent_info_and_write2db(orders_after_download_ent_list,'贵阳大数据')
            first_try.write_to_json_file(record_file,orders_after_download_ent_info)



if __name__ == '__main__':
    config_file = 'order.xml'
    record_file = 'record.json'