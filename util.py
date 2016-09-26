#!/usr/bin/env python
# encoding: utf-8


import dpkt
import socket
import random


def mac_addr(address):
    return ':'.join('%02x' % ord(b) for b in address)


def ip_to_str(address):
    return socket.inet_ntop(socket.AF_INET, address)


def print_packet(pkt):
    ip = dpkt.ip.IP(pkt.packet.get_payload())
    if ip.p == dpkt.ip.IP_PROTO_TCP:
        syn = bool(ip.tcp.flags & dpkt.tcp.TH_SYN)
        fin = bool(ip.tcp.flags & dpkt.tcp.TH_FIN)
        # Print out the info
        print pkt.timestamp,
        print '%s:%d -> %s:%d   (len=%d ttl=%d SYN=%d FIN=%d)\n' % \
            (ip_to_str(ip.src), ip.tcp.sport, ip_to_str(ip.dst), ip.tcp.dport,
                ip.len, ip.ttl, syn, fin)
        if ip.tcp.data != "":
            print "data: %s\n" % (ip.tcp.data)


def rand_latency(latency):
    rl = random.randrange(0, latency, 1)
    return rl
