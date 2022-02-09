#!/usr/bin/env python
# -*- coding:UTF-8 -*-

import requests
from prometheus_client import start_http_server  # ,Summary,Counter,Gauge,Histogram,CollectorRegistry
from prometheus_client.core import REGISTRY, GaugeMetricFamily  # ,CounterMetricFamily
import time


def getUrlData(url):
    r = requests.get(url)
    result_data = r.json()
    result = result_data['beans'][0]['VolumeFailuresTotal']
    return result


def get_used(url):
    r = requests.get(url).json()
    capacityused = float(r['beans'][0]['CapacityUsed'])
    capacitytotal = float(r['beans'][0]['CapacityTotal'])
    result = capacityused / capacitytotal
    return result


url1 = 'http://namenode01:50070/jmx?qry=Hadoop:service=NameNode,name=FSNamesystemState'
url2 = 'http://namenode02:50070/jmx?qry=Hadoop:service=NameNode,name=FSNamesystemState'
url3 = 'http://192.168.xxx.xxx:50070/jmx?qry=Hadoop:service=NameNode,name=FSNamesystemState'

class processCollector(object):
    def collect(self):
        bigVolumeStatus = float(getUrlData(url1))
        mpVolumeStatus = float(getUrlData(url2))
        reportUsedStatus = get_used(url3)
        bigUsedStatus = get_used(url1)
        mpUsedStatus = get_used(url2)
        yield GaugeMetricFamily('bigVolumeStatus', 'bigCluster', value=bigVolumeStatus)
        yield GaugeMetricFamily('mpVolumeStatus', 'mpCluster', value=mpVolumeStatus)
        yield GaugeMetricFamily('reportUsedStatus', 'reportCluster', value=reportUsedStatus)
        yield GaugeMetricFamily('bigUsedStatus', 'bigCluster', value=bigUsedStatus)
        yield GaugeMetricFamily('mpUsedStatus', 'mpCluster', value=mpUsedStatus)


REGISTRY.register(processCollector())

if __name__ == '__main__':
    start_http_server(23333)
    while True: time.sleep(10)
