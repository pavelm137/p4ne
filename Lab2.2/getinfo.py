#!/usr/bin/python3

from flask import Flask, jsonify
import glob
import re
import ipaddress


hosts = {}
app = Flask(__name__)


def create_html_table(table: list) -> str:
    output = "<table>"
    for n, row in enumerate(table):
        output += "<tr>"
        tag1 = "<th>" if n == 0 else "<td>"
        tag2 = "</th>" if n == 0 else "</td>"
        if type(row) is list:
            for col in row:
                output += tag1 + str(col) + tag2
        else:
            output += tag1 + str(row) + tag2
        output += "</tr>"
    output += "</table>"
    return output


@app.route('/')
def index():
    return "List of hosts in <a href=/configs>text table</a> or <a href=/json/configs>json</a> formats"


@app.route('/configs')
def configs():
    table_header = [["host", "interfaces"]]
    table_body = [[h, f"<a href=/config/{h}>text<a> <a href=/json/config/{h}>json<a>"] for h in hosts]
    return create_html_table(table_header + table_body)


@app.route('/json/configs')
def json_configs():
    return jsonify(list(hosts.keys()))


@app.route('/config/<hostname>')
def hostname(hostname):
    return create_html_table([f"IP Addresses of host {hostname}:"] + list(hosts[hostname]['addresses']))


@app.route('/json/config/<hostname>')
def json_hostname(hostname):
    return jsonify([str(a) for a in hosts[hostname]['addresses']])


if __name__ == '__main__':
    for f_name in glob.glob("/home/pm/tmp/config_files/*.log"):
        match = re.search(r".*/\d+\.\d+\.\d+\.\d+_(.+)\.log", f_name)
        hostname = match.group(1)
        hosts[hostname] = {}
        hosts[hostname]['addresses'] = set()
        with open(f_name) as f:
            for cur_line in f:
                if "ip address" in cur_line:
                    match = re.search(r"\b(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\b", cur_line)
                    if match:
                        hosts[hostname]['addresses'].add(ipaddress.IPv4Interface(match.groups()))
    app.run(debug=True)