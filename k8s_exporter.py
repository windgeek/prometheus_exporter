#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by wind on 2021/1/19

import subprocess
from prometheus_client import start_http_server  # ,Summary,Counter,Gauge,Histogram,CollectorRegistry
from prometheus_client.core import REGISTRY, GaugeMetricFamily  # ,CounterMetricFamily
import time


def cmdout(cmd):
    try:
        out_text = subprocess.check_output(cmd, shell=True).decode('utf-8')
    except subprocess.CalledProcessError as e:
        out_text = e.output.decode('utf-8')
        code = e.returncode
    return out_text


def dictpro(names, values):
    nvs = zip(names, values)
    nvDict = dict((name, value) for name, value in nvs)
    return nvDict


def scmd(node):
    re = cmdout('''
            kubectl get nodes | grep {} | grep {} | awk '{{print $2}}'
            '''.format(node, node)).strip()
    return re


def sscmd(node):
    re = cmdout('''
            kubectl get cs | grep {} | awk '{{print $2}}'
            '''.format(node)).strip()
    return re


def re2n(node):
    if scmd(node) == 'Ready':
        value = 1
    else:
        value = 0
    return value


def rre2n(service):
    if sscmd(service) == 'Healthy':
        value = 1
    else:
        value = 0
    return value


class statusCollector(object):
    def collect(self):
        status, health, status_gauges = {}, {}, {}
        # kubectl get nodes | grep k8s-145103 | grep k8s-145103 | awk '{print $2}'
        status_keys = ['k8s_145103', 'k8s_145104', 'k8s_145246']
        status_value = [re2n('k8s-145103'), re2n('k8s-145104'), re2n('k8s-145246')]
        status = dictpro(status_keys, status_value)
        print(status)
        health_keys = ['controller_manager', 'scheduler', 'etcd_0']
        health_value = [rre2n('controller-manager'), rre2n('scheduler'), rre2n('etcd-0')]
        health = dictpro(health_keys, health_value)
        print(health)
        for key in status:
            status_gauges[key] = GaugeMetricFamily('k8sNodeStatus_{}'.format(key), 'k8sNode_status', value=status[key])
        for key in health:
            status_gauges[key] = GaugeMetricFamily('k8sServiceHealth_{}'.format(key), 'k8sService_health', value=health[key])
        for metric in status_gauges:
            yield status_gauges[metric]


if __name__ == '__main__':
    start_http_server(23337)
    REGISTRY.register(statusCollector())

    while True:
        time.sleep(10)
