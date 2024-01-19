#!/usr/bin/python3

from ipaddress import IPv4Network
import random


class IPv4RandomNetwork(IPv4Network):
    def __init__(self):
        rand_network = random.randint(0x0B000000, 0xDF000000)
        rand_prefix = random.randint(8, 24)
        IPv4Network.__init__(self, (rand_network, rand_prefix), strict=False)

    def regular(self):
        if self.is_global and not (self.is_link_local or self.is_loopback or self.is_multicast or self.is_private or self.is_reserved or self.is_unspecified):
            return True
        return False

    def key_value(self):
        return int(self.netmask) * 2 ** 32 + int(self.network_address)


networks = set()
while len(networks) < 50:
    net = IPv4RandomNetwork()
    if net.regular():
        networks.add(net)

for net in sorted(networks, key=IPv4RandomNetwork.key_value):
    print(net)
