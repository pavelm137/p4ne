#!/usr/bin/python3

from pysnmp.hlapi import *

def print_results(results):
    for result in results:
        error_indication, error_status, error_index, var_binds = result
        for var in var_binds:
            print(var)


ip_addr = '10.31.70.209'
snmp_port = 161
snmp_sysdescr = ObjectIdentity('SNMPv2-MIB', 'sysDescr', 0)
snmp_ifaces = ObjectIdentity('1.3.6.1.2.1.2.2.1.2')

res_sysdescr = getCmd(
    SnmpEngine(),
    CommunityData('public', mpModel=0),
    UdpTransportTarget((ip_addr, snmp_port)),
    ContextData(),
    ObjectType(snmp_sysdescr)
)
res_ifaces = nextCmd(
    SnmpEngine(),
    CommunityData('public', mpModel=0),
    UdpTransportTarget((ip_addr, snmp_port)),
    ContextData(),
    ObjectType(snmp_ifaces), lexicographicMode=False
)

print("sysdescr:")
print_results(res_sysdescr)
print("")
print("Interfaces:")
print_results(res_ifaces)
