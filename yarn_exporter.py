#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by wind on 2021/1/19

import requests
from requests.auth import HTTPBasicAuth
import json
from prometheus_client import start_http_server  # ,Summary,Counter,Gauge,Histogram,CollectorRegistry
from prometheus_client.core import REGISTRY, GaugeMetricFamily  # ,CounterMetricFamily
import time


def app_runtime(appname):
    base_url = "http://172.28.9.6:8443/ws/v1/cluster/apps"
    # print(base_url)
    auth = HTTPBasicAuth('yuhang.zhao', 'Ipinyou_2020')
    r = requests.get(base_url, auth=auth, verify=False)
    # response = json.loads(r.content)
    return r


def dictpro(names, values):
    nvs = zip(names, values)
    nvDict = dict((name, value) for name, value in nvs)
    return nvDict


# class lagCollector(object):
#     def collect(self):
#         l1 = ['dtss-platform-clk', 'dtss-realtime-base', 'dtss-stats-cvt', 'dtss-realtime-account']
#         # 不支持含有-的str做key，l1直接用有问题，转化成_
#         l1l = [i.replace('-', '_') for i in l1]
#         l2 = []
#         for i in l1:
#             l2.append(get_lag('td_kafka', 'rpt', i))
#         print(l2)
#         lags = dictpro(l1l, l2)
#         lagsgauge = {}
#         for key in lags:
#             lagsgauge[key] = GaugeMetricFamily(key, 'rpt', value=lags[key])
#         for metric in lagsgauge:
#             yield lagsgauge[metric]


if __name__ == '__main__':
    # start_http_server(23333)
    # REGISTRY.register(lagCollector())
    #
    # while True:
    #     time.sleep(10)
    app_runtime('realTimeBaseAgg2RptbaseTask-100')