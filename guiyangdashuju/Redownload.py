#-*- coding: UTF-8 -*-
import json
import re

class ReDownload(object):
    def __init__(self, record_file):
        pass

    def parse_record_file(self, record_file):
        with open(record_file, 'r', encoding='utf-8') as file:
            list_of_order_status = json.load(file)
            print(list_of_order_status)
        return list_of_order_status

    def check_order_status(self, list_of_order_status):
        for each in list_of_order_status:
            tag = each['tag']
            saved = each['saved']
            total = each['total']
            get_ent_list = each['get_ent_list']
            ent_list_filename = each['ent_list_filename']



            if get_ent_list and saved != total:
                # 企业详细信息没有下载完毕
                self.extract_enterprise_from_file(ent_list_filename)

    def extract_enterprise_from_file(self, ent_list_filename):
        with open(ent_list_filename, 'r', encoding='utf-8') as file:
            content = file.read()
            result = {}
            ent_id = re.findall('"ent_id":"(\d{0,10})"', content, re.S)
            entname = re.findall('"entname":"(.*?)"', content, re.S)
            for m,n in zip(ent_id, entname):
                result[n] = m  # 格式：'佛山市三水恒昌华泰小额贷款有限公司': '8700178'
        # print('一共有效下载{}条企业信息'.format(len(result)))
        logging.warning('一共有效下载{}条企业信息'.format(len(result)))
        return result

    def download_ent_info_and_write2db(self, orders, db_name):
        db = MongoDB.DataBase(db_name).get_db_handle()

        for each in orders:
            ent_info_dirname = each['ent_info_dirname']
            tag = each['tag']
            token_id = each['token_id']
            ent_list_filename = each['ent_list_filename']
            ent_info_url = each['ent_info_url']
            order_status = each['order_status']
            success_count = 0

            try:
                if order_status['get_ent_list'] == 0: # 跳过企业列表下载失败的订单
                    continue
                all_enterprise = self.extract_enterprise_from_file(ent_list_filename)
                logging.warning('正在查询全部企业的详细信息')
                db_sheet = db[tag + '-' + ent_info_dirname] # 构造Mongodb中的数据表

                for ent_name, ent_id in all_enterprise.items():
                    temp = '\"organizationid\":\"{}\"'.format(ent_id)
                    parameters = '{%s}' %temp  #例子：parameters = "{\"organizationid\":\"5115801\"}"
                    para = {
                        'tokenId': token_id,
                        'encryptdata': parameters
                    }
                    response = requests.post(ent_info_url, params=para)
                    content = json.loads(response.text)
                    if content['rescode'] != '00000':
                        logging.error('存在错误，下载失败：{}'.format(content))
                        raise CrawlError()
                    # print(content)
                    print('正在写入数据库：{}'.format(ent_name))
                    db_sheet.insert_one({'ent_name':ent_name, 'info':str(content)})
                    success_count += 1
                    time.sleep(1.5)
                else:
                    order_status['saved'] = success_count

            except Exception as e:
                order_status['saved'] = success_count
                logging.error(e)
                continue
        return orders

