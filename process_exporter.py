#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by wind on 2021/1/19

import subprocess
from prometheus_client import start_http_server  # ,Summary,Counter,Gauge,Histogram,CollectorRegistry
from prometheus_client.core import REGISTRY, GaugeMetricFamily  # ,CounterMetricFamily
import time


def cmdout(cmd):
    try:
        out_text = int(subprocess.check_output(cmd, shell=True).decode('utf-8'))
    except subprocess.CalledProcessError as e:
        out_text = e.output.decode('utf-8')
    return out_text


def dictpro(names, values):
    nvs = zip(names, values)
    nvDict = dict((name, value) for name, value in nvs)
    return nvDict


def process_find():
    process_num = cmdout("ps aux|grep jelly | grep -v grep |grep -v jelly_exporter.py|wc -l")
    return process_num



class statusCollector(object):
    def collect(self):
        status, status_gauges = {}, {}
        status_keys = ['jelly']
        status_value = [process_find()]
        status = dictpro(status_keys, status_value)
        for key in status:
            status_gauges[key] = GaugeMetricFamily('jelly_status_{}'.format(key), 'jelly_status', value=status[key])
        for metric in status_gauges:
            yield status_gauges[metric]


if __name__ == '__main__':
    start_http_server(23335)
    REGISTRY.register(statusCollector())

    while True:
        time.sleep(10)
