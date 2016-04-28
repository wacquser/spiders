import requests

def get_ip():
    # http://qsdrk.daili666api.com/ip/?tid=557589527786211&num=2&delay=1&category=2&filter=on
    url = 'http://qsdrk.daili666api.com/ip/'
    paramaters = {
        'tid':557589527786211,
        'num':2,
        'category':2,
        'filter':'on'
    }
    response = requests.get(url, params=paramaters)
    return response.text

def write_to_file(content):
    with open('ip.txt', 'w') as file:
        for each in content.split('\r\n'):
            result = '{\'ip_port\': \'%s\', \'user_pass\': \'\'},' % each.strip('\n')
            file.write(result)

if __name__ == '__main__':
    write_to_file(get_ip())




