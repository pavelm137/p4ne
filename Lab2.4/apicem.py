#!/usr/bin/python3

import requests
from flask import Flask, jsonify

hosts = {}
app = Flask(__name__)


@app.route('/api/topology')
def topology():
    return jsonify(processes_top10)


host_ip = "10.31.70.209"
login = 'restapi'
password = 'j0sg1280-7@'
api_url = '/restconf/data/Cisco-IOS-XE-process-memory-oper:memory-usage-processes'
requests.packages.urllib3.disable_warnings()
headers = {
    "accept": "application/yang-data+json",
    "Content-Type": "application/yang-data+json"
}
uri = 'https://' + host_ip + api_url

sort_key = "holding-memory"
resp = requests.get(uri, auth=(login, password), headers=headers, verify=False)
processes_all = resp.json()['Cisco-IOS-XE-process-memory-oper:memory-usage-processes']['memory-usage-process']
processes_all_sorted = sorted(processes_all, key=lambda x: int(x[sort_key]), reverse=True)
processes_top10 = processes_all_sorted[:10]
col_w = 25
print(f'{"Process name":{col_w}}{sort_key:{col_w}}')
for proc in processes_top10:
    print(f'{proc["name"]:{col_w}}{proc[sort_key]:{col_w}}')

app.run(debug=True)