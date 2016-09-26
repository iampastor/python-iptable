#!/bin/bash

function start(){
    iptables -A INPUT -i lo -p tcp --dport $1 -j NFQUEUE --queue-num 1
}

function stop(){
    iptables -F
}

case $1 in
    start)
        start $2
        ;;
    stop)
        stop
        ;;
esac
