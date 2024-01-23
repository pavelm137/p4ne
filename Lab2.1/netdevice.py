#!/usr/bin/python3

import paramiko
import time
import requests
import re


HOST_IP="10.31.70.209"
LOGIN = 'restapi'
PASSWORD = 'j0sg1280-7@'
BUF_SIZE = 20000
TIMEOUT = .5
# to suppress InsecureRequestWarning:
requests.packages.urllib3.disable_warnings()

# using CLI:

print("\nUsing CLI:\n")
try:
    ssh_connection = paramiko.SSHClient()
    ssh_connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_connection.connect(HOST_IP, username=LOGIN, password=PASSWORD, look_for_keys=False, allow_agent=False)
    session = ssh_connection.invoke_shell()

    session.send("\n")
    time.sleep(TIMEOUT)
    session.recv(BUF_SIZE)
    session.send("terminal length 0\n")
    time.sleep(TIMEOUT)
    session.recv(BUF_SIZE)
    session.send("show interface\n")
    time.sleep(TIMEOUT)
    show_int_output = session.recv(BUF_SIZE).decode()
    print("interface        in packets  in bytes    out packets out bytes")
    for line in show_int_output.split('\n'):
        match = re.search("^(\w+) is", line)
        if match:
            print(f"{match.group(1):17}", end="")
        match = re.search("(\d+) packets input, (\d+) bytes", line)
        if match:
            print(f"{match.group(1):12}{match.group(2):12}", end="")
        match = re.search("(\d+) packets output, (\d+) bytes", line)
        if match:
            print(f"{match.group(1):12}{match.group(2):12}")
    session.close()
except paramiko.ssh_exception.NoValidConnectionsError:
    print("SSH hung :-(")

# Using REST:

headers = {
    "accept": "application/yang-data+json",
    "Content-Type": "application/yang-data+json"
}
url = 'https://' + HOST_IP + '/restconf/data/Cisco-IOS-XE-interfaces-oper:interfaces'
resp = requests.get(url, auth=(LOGIN, PASSWORD), headers=headers, verify=False)
interfaces = resp.json()['Cisco-IOS-XE-interfaces-oper:interfaces']['interface']
print("\nUsing REST:\n")
print("interface        in packets  in bytes    out packets out bytes")
for iface in interfaces:
    istat = iface['statistics']
    print(f"{iface['name']:17}{istat['in-unicast-pkts']:12}{istat['in-octets']:12}{istat['out-unicast-pkts']:12}{str(istat['out-octets']):12}")

