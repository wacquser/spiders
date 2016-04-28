import requests


# proxies = {
#   "http": "http://10.10.1.10:3128",
#   "https": "http://10.10.1.10:1080",
# }
# # 106.60.81.51:80
#
# requests.get("http://example.org", proxies=proxies)

url = 'http://httpbin.org/ip'
proxies = {}
# headers = {
#         'Connection':'keep-alive',
#         'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36',
#         }
headers={
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate, sdch',
            'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4',
            'Cache-Control':'max-age=0',
            'Connection':'keep-alive',
            'Host':'httpbin.org',
            'Upgrade-Insecure-Requests':1,
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'
        }
# with open('ip.txt', 'r') as file:
# with open('youdaili.txt', 'r') as file:
with open('goumai.txt', 'r') as file:
    for each in file:
        proxies['http'] = 'http://%s' % each.strip()
        print proxies
        try:
            response = requests.get(url, proxies = proxies, headers=headers)
            print response.text, response.status_code
        except:
            continue
