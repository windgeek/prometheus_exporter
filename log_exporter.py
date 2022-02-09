#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by wind on 2020/4/14

from prometheus_client import start_http_server  # ,Summary,Counter,Gauge,Histogram,CollectorRegistry
from prometheus_client.core import REGISTRY, GaugeMetricFamily  # ,CounterMetricFamily
import time
import re
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

def appear(logname, error):
    f = open(logname)
    for i in f:
        l = re.search(error, i, re.IGNORECASE)
        if l:
            status = 1
            # log_str = i
        else:
            status = 0
    f.close()
    return status


def disappear(logname, success):
    f = open(logname)
    for i in f:
        l = re.search(success, i, re.IGNORECASE)
        if l:
            status1 = 1
        else:
            status1 = 0
    f.close()
    return status1


class logCollector(object):
    def collect(self):
        appearError = appear("/data/mdp-logs/ing/mdp.sys.log", "线索job拉到的数据少于最小值可能不正常")
        yield GaugeMetricFamily('appearError_data', '拉到数据少于最小值', value=appearError)
        # yield GaugeMetricFamily('errorDetails', '拉到数据少于最小值的日志详情', value=errorDetails)
        disappearSuccess_cep = disappear("/data/mdp-logs/ing/mdp.sys.log", "cep-leads-puller结束执行")
        yield GaugeMetricFamily('disappearSuccess_cep', 'cep-leads-puller结束执行', value=disappearSuccess_cep)
        disappearSuccess_dcs = disappear("/data/mdp-logs/ing/mdp.sys.log", "dcs-leads-puller结束执行")
        yield GaugeMetricFamily('disappearSuccess_dcs', 'dcs-leads-puller结束执行', value=disappearSuccess_dcs)


if __name__ == '__main__':
    start_http_server(22333)
    REGISTRY.register(logCollector())
    while True: time.sleep(10)
