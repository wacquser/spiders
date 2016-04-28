import requests
from bs4 import BeautifulSoup
import re


class Xicidaili(object):
    def __init__(self):
        self.url = ['http://www.xicidaili.com/nn/','http://www.xicidaili.com/nt/']

    def download(self):
        headers = {
        'Connection':'keep-alive',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36',
        }
        file = open('ip.txt', 'a+')
        for each in self.url:

            response = requests.get(each, headers=headers)
            soup = BeautifulSoup(response.text, 'lxml')
            selector = soup.select('table tr')
            print len(selector)

            for each in selector:
                # row = each.select('td')
                # print row
                ip_addr = re.findall('<td>(\d{0,3}\.\d{0,3}\.\d{0,3}\.\d{0,3})</td>', str(each), re.S)
                if not ip_addr:
                    continue
                ip_addr = ip_addr[0]
                port = re.findall('<td>(\d{1,5})</td>', str(each), re.S)[0]
                speed_and_time = re.findall('<div class="bar" title="(\d\.\d{0,3}).*?">', str(each), re.S)
                speed = speed_and_time[0]
                if float(speed) < 1.0:
                    print ip_addr, port
                    file.write(ip_addr + ':' + port+'\n')
                    # print ip_addr, port, speed_and_time
        file.close()




if __name__ == '__main__':
    test = Xicidaili()
    test.download()
