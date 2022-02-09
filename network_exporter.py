#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by wind on 2021/1/12

from prometheus_client import start_http_server  # ,Summary,Counter,Gauge,Histogram,CollectorRegistry
from prometheus_client.core import REGISTRY, GaugeMetricFamily  # ,CounterMetricFamily
import subprocess
import time


def cmdout(cmd):
    try:
        out_text = subprocess.check_output(cmd, shell=True).decode('utf-8')
    except subprocess.CalledProcessError as e:
        out_text = e.output.decode('utf-8')
        code = e.returncode
    return out_text


# 不继承object对象，只拥有了__doc__ , __module__ 和 自己定义的变量
# 继承了object对象，拥有了好多可操作对象，这些都是类中的高级特性。
# 基于python 2.7.10版本，实际上在python 3 中已经默认就帮你加载了object了（即便你没有写上object）
class networkCollector(object):
    def collect(self):
        cmd = '''ping -c 4 -w 1 -i 0.5 192.168.xxx.xxx | grep "packet loss" | awk '{print $6}'
        '''
        packetloss = float(cmdout(cmd).strip('%')[0])
        yield GaugeMetricFamily('packetloss_xxxtoxxx', 'network', value=packetloss)


if __name__ == '__main__':
    start_http_server(23333)
    REGISTRY.register(networkCollector())
    while True:
        time.sleep(1)
