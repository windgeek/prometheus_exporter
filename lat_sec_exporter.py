#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by wind on 2021/1/19

import requests
from prometheus_client import start_http_server  # ,Summary,Counter,Gauge,Histogram,CollectorRegistry
from prometheus_client.core import REGISTRY, GaugeMetricFamily  # ,CounterMetricFamily
import time
import json



def api_get(psql):
    url = "http://172.28.8.25:9090/api/v1/query?query={}".format(psql)
    r = requests.get(url)
    decode = json.loads(r.text)
    print(decode)
    value = decode['data']['result'][0]['value'][1]
    return int(value)


def dictpro(names, values):
    nvs = zip(names, values)
    nvDict = dict((name, value) for name, value in nvs)
    return nvDict


class statusCollector(object):
    def collect(self):
        pday = time.strftime('%Y%m%d', time.localtime())
        bid_nodeal_suc_psql = 'sum(m__data_v6_logs_bid_nodeal_1_bid_nodeal__log__success_line_count_total{{day="{}"}})'.format(pday)
        unbid_nodeal_suc_psql = 'sum(m__data_v6_logs_unbid_nodeal_1_unbid_nodeal__log__success_line_count_total{{day="{}"}})'.format(pday)
        algo_pre_bid_suc_psql = 'sum(m__data_v6_logs_algo_pre_bid_rec_0_pre_bid_rec__log__success_line_count_total{{day="{}"}})'.format(pday)
        unbid_deal_suc_psql = 'sum(m__data_v6_logs_unbid_deal_1_unbid_deal__log__success_line_count_total{{day="{}"}})'.format(pday)
        bid_deal_suc_psql = 'sum(m__data_v6_logs_bid_deal_1_bid_deal__log__success_line_count_total{{day="{}"}})'.format(pday)
        print(bid_nodeal_suc_psql, unbid_nodeal_suc_psql, algo_pre_bid_suc_psql, unbid_deal_suc_psql, bid_deal_suc_psql)
        api_get(bid_nodeal_suc_psql)
        status, status_gauges = {}, {}
        status_keys = ['bid_nodeal_suc', 'unbid_nodeal_suc', 'algo_pre_bid_suc', 'unbid_deal_suc_psql', 'bid_deal_suc']
        status_value = [api_get(bid_nodeal_suc_psql), api_get(unbid_nodeal_suc_psql), api_get(algo_pre_bid_suc_psql), api_get(unbid_deal_suc_psql), api_get(bid_deal_suc_psql)]
        status = dictpro(status_keys, status_value)
        for key in status:
            status_gauges[key] = GaugeMetricFamily('lat_adp_{}'.format(key), 'lat_adp', value=status[key])
        for metric in status_gauges:
            yield status_gauges[metric]


if __name__ == '__main__':
    start_http_server(25333)
    REGISTRY.register(statusCollector())

    while True:
        time.sleep(10)

