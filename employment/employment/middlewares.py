import random
import base64
from settings import PROXIES
from settings import REDIS_NUM
from RedisQueue import RedisQueue
from DownloadIP import get_ip


class RandomUserAgent(object):
    """Randomly rotate user agents based on a list of predefined ones"""

    def __init__(self, agents):
        self.agents = agents

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.getlist('USER_AGENTS'))

    def process_request(self, request, spider):
        # print "**************************" + random.choice(self.agents)
        request.headers.setdefault('User-Agent', random.choice(self.agents))


class ProxyMiddleware(object):
    def process_request(self, request, spider):
        proxy = random.choice(PROXIES)
        if proxy['user_pass'] is not None:
            request.meta['proxy'] = "http://%s" % proxy['ip_port']

            encoded_user_pass = base64.encodestring(proxy['user_pass'])
            request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass
            print "**************ProxyMiddleware have pass************" + proxy['ip_port']
        else:
            print "**************ProxyMiddleware no pass************" + proxy['ip_port']
            request.meta['proxy'] = "http://%s" % proxy['ip_port']


import logging
logger = logging.getLogger(__name__)


class RedisProxyMiddleware(object):

    def select_ip(REDIS_NUM):
        redis_list = []
        for i in range(REDIS_NUM):
            redis_list.append(RedisQueue('proxy_ip_%d' %i))
        for each in redis_list:
            print each.key
        label = random.choice(range(REDIS_NUM))
        while redis_list[label].empty():
            label = random.choice(range(REDIS_NUM))
        proxy_ip = redis_list[label].get()
        redis_list[label].put(proxy_ip)
        return proxy_ip,label


    def process_request(self, request, spider):
        # proxy_ip,redis_label = self.select_ip(REDIS_NUM)
        redis_list = []
        for i in range(REDIS_NUM):
            redis_list.append(RedisQueue('proxy_ip_%d' %i))
        redis_label = random.choice(range(REDIS_NUM))
        while redis_list[redis_label].empty():
            redis_label = random.choice(range(REDIS_NUM))
        proxy_ip = redis_list[redis_label].get()
        redis_list[redis_label].put(proxy_ip)

        proxy_para = {
                'ip_port': proxy_ip,
                'user_pass': ''
            }
        request.meta['proxy'] = "http://%s" % proxy_para['ip_port']
        request.meta['redis_label'] = redis_label
        if proxy_para['user_pass'] is not None:
            encoded_user_pass = base64.encodestring(proxy_para['user_pass'])
            request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass
        print "*********************** RedisProxyMiddleware Using proxy ip: %s *****" % proxy_para['ip_port']

    def process_request_origin(self, request, spider):
        redis = RedisQueue('proxy_ip')
        if not redis.empty():
            proxy_ip = redis.get()
        else:
            proxy_ip = get_ip()

        proxy_para = {
                'ip_port': proxy_ip,
                'user_pass': ''
            }
        request.meta['proxy'] = "http://%s" % proxy_para['ip_port']
        if proxy_para['user_pass'] is not None:
            encoded_user_pass = base64.encodestring(proxy_para['user_pass'])
            request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass
        print "*********************** RedisProxyMiddleware Using proxy ip: %s *****" % proxy_para['ip_port']
        redis.put(proxy_ip)


class InvalidRequestMiddleware(object):

    def process_response(self, request, response, spider):
        return response

    def dispose_ip(self, proxy_ip, redis_label):
        redis_list = []
        for i in range(REDIS_NUM):
            redis_list.append(RedisQueue('proxy_ip_%d' %i))
        redis_invalid_ip = RedisQueue('invalid_ip')
        if redis_label == REDIS_NUM - 1:
            redis_invalid_ip.put(proxy_ip)
            redis_list[0].put(get_ip())
        else:
            redis_list[redis_label].remove(proxy_ip)
            redis_list[redis_label+1].put(proxy_ip)
            if redis_list[0].empty():
                redis_list[0].put(get_ip())

        new_redis_label = random.choice(range(REDIS_NUM))
        while redis_list[new_redis_label].empty():
            new_redis_label = random.choice(range(REDIS_NUM))
        new_proxy_ip = redis_list[new_redis_label].get()
        redis_list[new_redis_label].put(new_proxy_ip)
        return new_proxy_ip,new_redis_label

    def process_exception1(self, request, exception, spider):
        request_ip = request.meta['proxy']
        invalid_ip = request_ip.split('//')[1]
        redis_label = request.meta['redis_label']
        new_proxy_ip, new_redis_label = self.dispose_ip(invalid_ip, redis_label)

        print '+++++++++++++++++++++++%s' %exception
        print '-----------------------removing %s from proxy_ip_%d' %(invalid_ip, redis_label)
        proxy_para = {
            'ip_port': new_proxy_ip,
            'user_pass': ''
        }
        request.meta['proxy'] = "http://%s" % proxy_para['ip_port']
        request.meta['redis_label'] = new_redis_label
        if proxy_para['user_pass'] is not None:
            encoded_user_pass = base64.encodestring(proxy_para['user_pass'])
            request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass
        print ">>>>>>>>>>>>>>>>>>>>>>>>>>> switch %s to ip: %s *****" % (invalid_ip,proxy_para['ip_port'])

    def process_exception(self, request, exception, spider):
        request_ip = request.meta['proxy']
        invalid_ip = request_ip.split('//')[1]
        redis = RedisQueue('proxy_ip')
        redis_invalid_ip = RedisQueue('invalid_ip')
        if not redis.empty():
            redis.remove(invalid_ip)
            redis_invalid_ip.put(invalid_ip)
            print '+++++++++++++++++++++++%s' %exception
            print '-----------------------removing ip from redis: %s' %invalid_ip

        new_ip = get_ip()
        proxy_para = {
            'ip_port': new_ip,
            'user_pass': ''
        }
        request.meta['proxy'] = "http://%s" % proxy_para['ip_port']
        if proxy_para['user_pass'] is not None:
            encoded_user_pass = base64.encodestring(proxy_para['user_pass'])
            request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass
        print ">>>>>>>>>>>>>>>>>>>>>>>>>>> switch %s to ip: %s *****" % (invalid_ip,proxy_para['ip_port'])
        redis.put(new_ip)


