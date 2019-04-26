#!/usr/bin/env python

# RITSEC Demos Week 13
# Bonus Challenge

from scapy.all import *

# interface and client list
interface = "wlan0mon"
clients = []

def sniffmgmt(p):
    """
    Find unique client MAC addresses from Scapy sniff output
    p: Scapy output to process
    """
    stamgmtstypes = (0, 2, 4)
    if p.haslayer(Dot11):
        if p.type == 0 and p.subtype in stamgmtstypes:
            if p.addr2 not in clients:
                print p.addr2
                clients.append(p.addr2)

# Use Scapy to capture wireless devices' MAC addresses
if __name__ == '__main__' :
    sniff(iface=interface, prn=sniffmgmt)