import requests
import base64
from redis_ip import RedisQueue

def tett():
    url = 'http://www.lagou.com'

    headers = {
        'User-Agent':"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)"
    }
    proxy = {
        # 'http':'http://211.144.76.58:9000'
        'http':'http://116.29.235.14:8118'
    }
    response = requests.get(url, proxies=proxy, headers=headers)
    print response.text

def process_request(self, request, spider):
    redis = RedisQueue('proxy_ip')
    if not redis.empty():
        proxy_ip = redis.get()
        # print proxy_ip
        proxy_para = {
            'ip_port': proxy_ip,
            'user_pass': ''
        }
        # print proxy_para
        if proxy_para['user_pass'] is not None:
            request.meta['proxy'] = "http://%s" % proxy_para['ip_port']
            encoded_user_pass = base64.encodestring(proxy_para['user_pass'])
            request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass
            print "**************ProxyMiddleware have pass************" + proxy_para['ip_port']
        else:
            print "**************ProxyMiddleware no pass************" + proxy_para['ip_port']
            request.meta['proxy'] = "http://%s" % proxy_para['ip_port']
        redis.put(proxy_ip)

# tett()

import random
import time
# while True:
#     print random.choice(range(1,4))
#     time.sleep(1)

def test_num(num):
    while True:
        print random.choice(range(num))
        time.sleep(1)

# test_num(3)

from RedisQueue import RedisQueue
import random
def select_ip(num):
    redis_list = []
    for i in range(num):
        redis_list.append(RedisQueue('proxy_ip_%d' %i))
    for each in redis_list:
        print each.key
    label = random.choice(range(num))
    while redis_list[label].empty():
        label = random.choice(range(num))
    proxy_ip = redis_list[label].get()
    return proxy_ip,label


a,b= select_ip(3)
print a,b
# cal(3)
