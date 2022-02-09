#!/usr/bin/env python
# -*- coding:UTF-8 -*-
import sys

import requests
from prometheus_client import start_http_server  # ,Summary,Counter,Gauge,Histogram,CollectorRegistry
from prometheus_client.core import REGISTRY, GaugeMetricFamily  # ,CounterMetricFamily
import time
import subprocess


def strpro(str):
    return int(str.split('=')[1])


def listpro(l):
    ln = []
    for i in range(1, len(l)):
        ln.append(strpro(l[i]))
    return ln


def dictpro(names, values):
    nvs = zip(names, values)
    nvDict = dict((name, value) for name, value in nvs)
    return nvDict


def getUrlData(url, p_tpye):
    r = requests.get(url)
    apt_counters = r.json()['result']['apt_counters']
    ptpye = str(apt_counters[p_tpye]).split(',')
    click, clickSucc, clickFaild, clickTimeOut, clickSave, clickSaveFaild, clickWrong, cvt, cvtCamp, clickFound, clickFoundFaild, report, reportMatch, reportSucc, reportFaild = listpro(
        ptpye)
    return click, clickSucc, clickFaild, clickTimeOut, clickSave, clickSaveFaild, clickWrong, cvt, reportMatch, reportSucc, reportFaild, clickFoundFaild


def cmdout(cmd):
    # ip = str(cmdout("ifconfig | grep -C 1 eth0 | grep -v grep | grep inet | awk '{print $2}'")).strip()
    try:
        out_text = subprocess.check_output(cmd, shell=True).decode('utf-8')
    except subprocess.CalledProcessError as e:
        out_text = e.output.decode('utf-8')
        code = e.returncode
    return out_text


class processCollector(object):
    def collect(self):
        ps = ['gdt', 'kuaishou', 'qutoutiao', 'iqiyi', 'toutiao']
        ip = str(cmdout("ifconfig | grep -C 1 eth0 | grep -v grep | grep inet | awk '{print $2}'")).strip()
        url = 'http://{}:8090/sys?key=12345'.format(ip)
        l1, l2, l3, l4, l5 = getUrlData(url, ps[0]), getUrlData(url, ps[1]), getUrlData(url, ps[2]), getUrlData(url, ps[3]), getUrlData(url, ps[4])
        lt = ['click', 'clickSucc', 'clickFaild', 'clickTimeOut', 'clickSave', 'clickSaveFaild', 'clickWrong', 'cvt',
              'reportMatch', 'reportSucc', 'reportFaild', 'clickFoundFaild']
        shoutao_gauges = {}
        gdt = dictpro(lt, l1)
        kuaishou = dictpro(lt, l2)
        qutoutiao = dictpro(lt, l3)
        iqiyi = dictpro(lt, l4)
        toutiao = dictpro(lt, l5)
        for key in gdt:
            shoutao_gauges[ps[0] + key] = GaugeMetricFamily(ps[0] + '_' + key, ps[0], value=gdt[key])
        for key in kuaishou:
            shoutao_gauges[ps[1] + key] = GaugeMetricFamily(ps[1] + '_' + key, ps[1], value=kuaishou[key])
        for key in qutoutiao:
            shoutao_gauges[ps[2] + key] = GaugeMetricFamily(ps[2] + '_' + key, ps[2], value=qutoutiao[key])
        for key in iqiyi:
            shoutao_gauges[ps[3] + key] = GaugeMetricFamily(ps[3] + '_' + key, ps[3], value=iqiyi[key])
        for key in toutiao:
            shoutao_gauges[ps[4] + key] = GaugeMetricFamily(ps[4] + '_' + key, ps[4], value=toutiao[key])
        for metric in shoutao_gauges:
            yield shoutao_gauges[metric]


if __name__ == '__main__':

    start_http_server(23333)
    REGISTRY.register(processCollector())

    while True:
        time.sleep(10)

