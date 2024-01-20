#!/usr/bin/python3

import ipaddress
import glob
import re


def parse_line(line):
    if "ip address" in line:
        match = re.search(r"\b(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\b", line)
        if match:
            return ipaddress.IPv4Interface(match.groups())
    return None


ips = set()
for f_name in glob.glob("/home/pm/tmp/config_files/*.log"):
    with open(f_name) as f:
        for cur_line in f:
            result = parse_line(cur_line)
            if result:
                ips.add(result)
for ip in ips:
    print(ip)
print(f'{len(ips)} unique addresses printed')
