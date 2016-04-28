import requests
import pickle
import xml.etree.ElementTree as etree
import json
import re
import os
import time
import pymongo

class ConnectionError(Exception): pass
class CrawlError(Exception):
    def __init__(self, location):
        with open('record.pickle', 'wb') as file:
            pickle.dump(location, file)

class Download(object):

    def __init__(self, config_file):
        client = pymongo.MongoClient('localhost', 27017)
        self.db = client['贵阳大数据']
        tree = etree.parse(config_file)
        root = tree.getroot()
        for each in root:
            order_id = each.find('order_id').text
            token_id = each.find('token_id').text
            tag = each.tag
            ent_list_url = each.find('enterprist_list/url').text
            ent_list_filename = tag + '/' +each.find('enterprist_list/file_name').text
            ent_info_url = each.find('enterprist_info/url').text
            ent_info_dirname = each.find('enterprist_info/dir').text

            if not os.path.exists(tag):
                os.mkdir(tag) # 创建目录
            if not os.path.exists(tag+'/'+ent_info_dirname):
                os.mkdir(tag+'/' + ent_info_dirname)
            # self.download_enterprise_list(token_id, ent_list_url, ent_list_filename, tag)
            self.download_enterprise_info(token_id, ent_info_url, ent_list_filename, ent_info_dirname, tag)

    def download_enterprise_list(self, token_id, ent_list_url, ent_list_filename, tag_name):
        print('正在查询订单：{}'.format(tag_name))
        para = {
            'tokenId': token_id
        }
        response = requests.post(ent_list_url, params=para)
        content = json.loads(response.text)
        if content['rescode'] != '00000': # 如果在返回结果中rescode的值不为00000，则说明返回的结果错误
            order = {'order_name':tag_name}
            print('查询有错误，错误信息如下：{}'.format(content))
            raise CrawlError()

        # 因为在服务器端设置了一次查询只能有200条结果，所以只能分批返回查询数据
        total_count = json.loads(content['encryptdata'])['total']
        print('查询到一共有{}条数据'.format(total_count))
        cycle_times = total_count // 200 + 2
        for i in range(1,  cycle_times):
            print('\t正在返回第{}页的结果'.format(i))
            temp = '\"pageIndex\":\"{}\", \"pageSize\":\"200\"'.format(i)
            paginator = '{%s}' %temp
            para = {
                'tokenId': token_id,
                'encryptdata': paginator
            }
            response = requests.post(ent_list_url, params=para)
            content = json.loads(response.text)
            if content['rescode'] != '00000':
                print('error')
            with open(ent_list_filename, 'a+', encoding='utf-8') as f: # 把结果写入到文件中
                f.write(str(content))
        print('{}的企业列表信息查询完成！'.format(tag_name))

    def extract_enterprise_from_file(self, ent_list_filename):
        with open(ent_list_filename, 'r', encoding='utf-8') as file:
            content = file.read()
            result = {}
            ent_id = re.findall('"ent_id":"(\d{0,10})"', content, re.S)
            entname = re.findall('"entname":"(.*?)"', content, re.S)
            for m,n in zip(ent_id, entname):
                result[n] = m  # 格式：'佛山市三水恒昌华泰小额贷款有限公司': '8700178'
        print('一共有效下载{}条企业信息'.format(len(result)))
        return result

    def download_enterprise_info(self, token_id, ent_info_url, ent_list_filename, ent_info_dirname, tag):
        all_enterprise = self.extract_enterprise_from_file(ent_list_filename)
        print('\n正在查询全部企业的详细信息')
        db_sheet = self.db[tag + '-' + ent_info_dirname]
        for ent_name, ent_id in all_enterprise.items():
            temp = '\"organizationid\":\"{}\"'.format(ent_id)
            parameters = '{%s}' %temp
            # parameters = "{\"organizationid\":\"5115801\"}"
            para = {
                'tokenId': token_id,
                'encryptdata': parameters
            }
            response = requests.post(ent_info_url, params=para)
            content = json.loads(response.text)
            if content['rescode'] != '00000':
                print('存在错误，下载失败：{}'.format(content))
                raise CrawlError()
            # print(content)
            print('正在写入数据库：{}'.format(ent_name))
            db_sheet.insert_one({'ent_name':ent_name, 'info':str(content)})
            # ent_file_name = tag + '/' + ent_info_dirname + '/'+ ent_name+'.txt'
            # with open( ent_file_name, 'w', encoding='utf-8') as file:
            #     file.write(str(content))
            time.sleep(1.5)



if __name__ == '__main__':
    temp = Download('order.xml')


