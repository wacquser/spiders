import pickle
import json
import xml.etree.ElementTree as etree
import logging

def pickle1():
    record = {'order':1, 'location':2}
    with open('record.pickle', 'wb') as file:
        pickle.dump(record, file)

def json1():
    record = [{'order':1, 'location':2},{'order':2, 'location':3}]
    with open('record.json', 'w', encoding='utf-8') as file:
        json.dump(record, file, indent=2)

def config():
    tree = etree.parse('order.xml')
    root = tree.getroot()
    write2file = []

    dir_name = '全部订单的企业列表'
    # if not os.path.exists(dir_name):
    #     os.mkdir(dir_name) # 创建目录
    for each in root:
        order_id = each.find('order_id').text
        token_id = each.find('token_id').text
        tag = each.tag
        ent_list_url = each.find('enterprist_list/url').text
        ent_list_filename = dir_name + '/' + tag + '-' +each.find('enterprist_list/file_name').text
        ent_info_url = each.find('enterprist_info/url').text
        ent_info_dirname = each.find('enterprist_info/dir').text
        status = {'tag':tag, 'total':0, 'saved':0}
        # json.dumps(status)
        with open('sb.json', 'a+', encoding='utf-8') as file:
            json.dump(status, file, ensure_ascii=False, indent=2)

def config_logging():
    # logging.basicConfig(level=logging.WARNING,
    #                     format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    #                     datefmt='%a, %d %b %Y %H:%M:%S',
    #                     filename='download.log',
    #                     filemode='w')

    root_logger= logging.getLogger()
    root_logger.setLevel(logging.WARNING) # or whatever
    handler = logging.FileHandler('test.log', 'w', 'utf-8') # or whatever
    formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s') # or whatever
    handler.setFormatter(formatter)
    root_logger.addHandler(handler)


    console = logging.StreamHandler()
    console.setLevel(logging.WARNING)
    formatter = logging.Formatter('%(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

def ttt():
    config_logging()
    logging.warning('你是一个四sb')
    logging.info('sssb')

# json1()
# config()
# config_logging()

def load_json():
    with open('record.json', 'r', encoding='utf-8') as file:
        entry = json.load(file)
        print(entry)

def test_list():
    temp = {'1':21,'2':32}
    print(temp[1:])

# load_json()
test_list()