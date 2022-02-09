#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by wind on 2021/1/12

from prometheus_client import start_http_server  # ,Summary,Counter,Gauge,Histogram,CollectorRegistry
from prometheus_client.core import REGISTRY, GaugeMetricFamily  # ,CounterMetricFamily
import subprocess
import time


def cmdout(node):
    try:
        cmd = '''curl -v http://192.168.152.28:7000/list/cc.antispam/ | grep -C 4 {} | grep 'text-align: right' | sed -n "2, 1p"
        '''.format(node)
        out_text = subprocess.check_output(cmd, shell=True).decode('utf-8').split('>')[1].replace(',', '').replace('</td', '')
        print(out_text)
    except subprocess.CalledProcessError as e:
        out_text = e.output.decode('utf-8')

    return int(out_text)


# 不继承object对象，只拥有了__doc__ , __module__ 和 自己定义的变量
# 继承了object对象，拥有了好多可操作对象，这些都是类中的高级特性。
# 基于python 2.7.10版本，实际上在python 3 中已经默认就帮你加载了object了（即便你没有写上object）
class antispamCollector(object):
    def collect(self):
        current_size, current_size_gauge = {}, {}
        current_size["node153119"] = cmdout("192.168.153.119:27200")
        current_size["node152193"] = cmdout("192.168.152.193:27200")
        current_size["node153114"] = cmdout("192.168.153.114:27200")
        current_size["node153115"] = cmdout("192.168.153.115:27200")
        current_size["node153112"] = cmdout("192.168.153.112:27200")
        current_size["node15275"] = cmdout("192.168.152.75:27200")
        current_size["node15276"] = cmdout("192.168.152.76:27200")
        current_size["node15228"] = cmdout("192.168.152.28:26000")
        current_size["node874"] = cmdout("172.28.8.74:27200")
        current_size["node875"] = cmdout("172.28.8.75:27200	")
        current_size["node2229"] = cmdout("172.28.2.229:27200")
        current_size["node2240"] = cmdout("172.28.2.240:27200")        	


        for key in current_size:
            current_size_gauge[key] = GaugeMetricFamily(key, 'antispam', value=current_size[key])
        for metric in current_size_gauge:
            yield current_size_gauge[metric]


if __name__ == '__main__':
    start_http_server(23333)
    REGISTRY.register(antispamCollector())
    while True:
        time.sleep(1)
