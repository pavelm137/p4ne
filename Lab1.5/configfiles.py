#!/usr/bin/python3

import glob

ips = set()
for fname in glob.glob("/home/pm/tmp/config_files/*.log"):
    with open(fname) as f:
        for cur_line in f:
            if "ip address" in cur_line:
                # убирает всё лишнее из строк вида 'ip address х.х.х.х х.х.х.х' и 'guest ip address х.х.х.х':
                cur_line = cur_line.replace("ip address", "").replace("guest", "").replace("sub", "").lstrip().rstrip()
                # если начинается и заканчивается числом, то с большой степенью вероятности это адрес или адрес и маска (возможны более глубокие проверки):
                if cur_line[0].isdigit() and cur_line[-1].isdigit():
                    ips.add(cur_line)
for ip in ips:
    print(ip)
