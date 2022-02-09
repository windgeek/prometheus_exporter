#!/data/python2.7.17/bin/python
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

def gitfile_find():
    gitfile = cmdout("find /root /home -name kworkers|wc -l")
    if gitfile == 0:
        return 0
    else:
        return gitfile


def certfile_find():
    certfile = cmdout("find /root -name cert.pem -o -name cert_key.pem | wc -l")
    if certfile == 0:
        return 0
    else:
        return certfile


def gtkfile_find():
    gtkfile = cmdout("find /tmp -name .GTK-unix|wc -l")
    if gtkfile == 0:
        return 0
    else:
        return gtkfile


def cronfile_find():
    cronfile = cmdout("grep -R 'kworkers' /var/spool/cron/ | wc -l")
    if cronfile == 0:
        return 0
    else:
        return cronfile


class statusCollector(object):
    def collect(self):
        status, status_gauges = {}, {}
        status_keys = ['xfile', 'certfile', 'gtkfile', 'cronfile']
        status_value = [gitfile_find(), certfile_find(), cronfile_find()]
        status = dictpro(status_keys, status_value)
        for key in status:
            status_gauges[key] = GaugeMetricFamily('ali_safe_status_{}'.format(key), 'ali_safe_status', value=status[key])
        for metric in status_gauges:
            yield status_gauges[metric]


if __name__ == '__main__':
    start_http_server(23339)
    REGISTRY.register(statusCollector())

    while True:
        time.sleep(10)
