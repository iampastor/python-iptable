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


config = None
q = Queue.Queue()
choices = []


class MyPacket:

    def __init__(self, packet):
        self.packet = packet
        self.timestamp = time.time()
        self.latency = 0

    def accept(self):
        self.packet.accept()

    def drop(self):
        self.packet.drop()

    def __str__(self):
        return str(self.packet)


def handle(pkt):
    mypkt = MyPacket(pkt)
    global config
    mypkt.latency = config.latency
    q.put(mypkt)


def init_choice(drop_rate):
    global choices
    for _ in range(drop_rate):
        choices.append(1)
    for _ in range(len(choices), 100):
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
                if config.v > 0:
                    print "Drop, latency: %d" % pkt.latency,
                pkt.drop()
            else:
                if config.v > 0:
                    print "Accept, latency: %d" % pkt.latency,
                pkt.accept()
            util.print_packet(pkt, config.v)
        else:
            q.put(pkt)


def parse_args():
    """--drop --latency -v
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--drop", default=0, type=int, help="drop rate")
    parser.add_argument("--latency", default=0, type=float, help="latency ms")
    parser.add_argument("-v", default=0, choices=[1, 2, 3], type=int, help="verbose output")
    args = parser.parse_args()
    global config
    config = args
    print "start at drop rate %s%%, latency %sms" % (config.drop, config.latency)


def main():
    parse_args()
    init_choice(config.drop)
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
