from redis_ip import RedisQueue

redis = RedisQueue('proxy_ip')
if not redis.empty():
    proxy_ip = redis.get()
    print proxy_ip
    proxy_para = {
        'ip_port': proxy_ip,
        'user_pass': ''
    }
    print proxy_para
    if proxy_para['user_pass'] is not None:
        # request.meta['proxy'] = "http://%s" % proxy_para['ip_port']
        # encoded_user_pass = base64.encodestring(proxy_para['user_pass'])
        # request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass
        print "**************ProxyMiddleware have pass************" + proxy_para['ip_port']
    else:
        print "**************ProxyMiddleware no pass************" + proxy_para['ip_port']
        # request.meta['proxy'] = "http://%s" % proxy_para['ip_port']

    # {'ip_port': '218.78.210.190:8080', 'user_pass': ''},
    redis.put(proxy_ip)
else:
    print 'empty'
# request.meta['proxy'] = 'http://%s' % proxy_ip['ip_port']
