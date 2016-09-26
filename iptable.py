#!/usr/bin/env python
# encoding: utf-8

import time
import threading
import Queue
import argparse
import atexit
import random

from netfilterqueue import NetfilterQueue

import util


drop_rate = 0
latency = 0
q = Queue.Queue()
choices = []


class MyPacket:

    def __init__(self, packet):
        self.packet = packet
        self.timestamp = time.time()

    def accept(self):
        self.packet.accept()

    def drop(self):
        self.packet.drop()

    def __str__(self):
        return str(self.packet)


def handle(pkt):
    mypkt = MyPacket(pkt)
    global latency
    mypkt.latency = util.rand_latency(latency)
    q.put(mypkt)


def init_choice(drop_rate):
    global choices
    for i in range(drop_rate):
        choices.append(1)
    for j in range(len(choices), 100):
        choices.append(0)


def is_drop():
    ch = random.choice(choices)
    return bool(ch)


def send_packet():
    while True:
        pkt = q.get()
        now = time.time()
        if (now - pkt.timestamp) * 1000 > pkt.latency:
            if is_drop():
                print "Drop, latency: %d" % pkt.latency,
                pkt.drop()
            else:
                print "Accept, latency: %d" % pkt.latency,
                pkt.accept()
            util.print_packet(pkt)
        else:
            q.put(pkt)


def parse_args():
    """--drop --latency
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--drop", default=0, type=int, help="drop rate")
    parser.add_argument("--latency", default=0, type=float, help="latency ms")
    args = parser.parse_args()
    global drop_rate, latency
    drop_rate = args.drop
    latency = args.latency
    print "start at drop rate %s%%, latency %sms" % (drop_rate, latency)


def main():
    parse_args()
    init_choice(drop_rate)
    atexit.register(clean)
    nfqueue = NetfilterQueue()
    sendThread = threading.Thread(target=send_packet)
    sendThread.setDaemon(True)
    sendThread.start()
    nfqueue.bind(1, handle)
    try:
        nfqueue.run()
    except KeyboardInterrupt:
        print


def clean():
    pass


if __name__ == "__main__":
    main()
