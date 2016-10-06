# 使用libnetfilter hook iptable，在本地进行延时或丢包，用于模拟

## 安装
1. `apt-get install build-essential python-dev libnetfilter-queue-dev`
2. `pip install -r requirements.txt`

## 使用
1. 开启iptable `iptables.sh start 8080`
2. 运行 `iptable.py --drop --latency`
3. 清除iptable `iptables.sh stop`


