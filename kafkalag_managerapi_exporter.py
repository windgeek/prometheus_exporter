#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by wind on 2021/1/19

import requests
from requests.auth import HTTPBasicAuth
import json
from prometheus_client import start_http_server  # ,Summary,Counter,Gauge,Histogram,CollectorRegistry
from prometheus_client.core import REGISTRY, GaugeMetricFamily  # ,CounterMetricFamily
import time


def get_lag(cluster_name, consumer_name, topic_name):
    config = {
        'cluster_name': cluster_name,
        'consumer_name': consumer_name,
        'topic_name': topic_name,
    }

    base_url = "http://172.28.9.3:8085/api/status/{cluster_name}/{consumer_name}/{topic_name}/KF/topicSummary".format(
                        **config)
    print(base_url)
    auth = HTTPBasicAuth('admin', 'xxxxxx')
    r = requests.get(base_url, auth=auth, verify=False)
    response = json.loads(r.content)['totalLag']
    return response


def dictpro(names, values):
    nvs = zip(names, values)
    nvDict = dict((name, value) for name, value in nvs)
    return nvDict


class lagCollector(object):
    def collect(self):
        l1 = ['dtss-platform-clk', 'dtss-realtime-base', 'dtss-stats-cvt', 'dtss-realtime-account']
        # 不支持含有-的str做key，l1直接用有问题，转化成_
        l1l = [i.replace('-', '_') for i in l1]
        l2 = []
        for i in l1:
            l2.append(get_lag('td_kafka', 'rpt', i))
        print(l2)
        lags = dictpro(l1l, l2)
        lagsgauge = {}
        for key in lags:
            lagsgauge[key] = GaugeMetricFamily(key, 'td_rpt', value=lags[key])
        for metric in lagsgauge:
            yield lagsgauge[metric]


if __name__ == '__main__':
    start_http_server(23333)
    REGISTRY.register(lagCollector())

    while True:
        time.sleep(10)
