

with open('goumai.txt', 'r') as file:
    for each in file:
        print '{\'ip_port\': \'%s\', \'user_pass\': \'\'},' % each.strip('\n')


# {'ip_port': '116.6.197.154:3128', 'user_pass': ''},