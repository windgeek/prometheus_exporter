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
        out_text = int(out_text)
    except subprocess.CalledProcessError as e:
        out_text = e.output.decode('utf-8')
        code = e.returncode
    return out_text


class lagCollector(object):
    def collect(self):
        lags, lags_gauges = {}, {}
# [root@emr-worker-1 ~]# kafka-consumer-groups.sh --bootstrap-server 172.28.9.1:9092 --group clk --describe
# Note: This will not show information about old Zookeeper-based consumers.

# TOPIC           PARTITION  CURRENT-OFFSET  LOG-END-OFFSET  LAG             CONSUMER-ID                                     HOST            CLIENT-ID
# dtss-dcs-clk    0          43706469        43708680        2211            consumer-1-5525cbb2-1c06-42e2-9c6f-49f4be45cb8c /172.28.9.8     consumer-1
# dtss-dcs-clk    1          118598465       118603050       4585            consumer-1-5525cbb2-1c06-42e2-9c6f-49f4be45cb8c /172.28.9.8     consumer-1
# dtss-dcs-clk    2          57727878        57732272        4394            consumer-1-5525cbb2-1c06-42e2-9c6f-49f4be45cb8c /172.28.9.8     consumer-1
        # 'dtss-platform-clk', 'dtss-realtime-base', 'dtss-stats-cvt', 'dtss-realtime-account'
        # kafka-consumer-groups.sh --bootstrap-server 172.28.9.1:9092 --group clk --describe | grep dtss-platform-cl | awk 'BEGIN{sum=0}{sum+=$5}END{print sum}'
        lags['dtss_platform_clk'] = cmdout("kafka-consumer-groups.sh --bootstrap-server 172.28.9.1:9092 --group {} "
                                           "--describe | grep {} | awk 'BEGIN{{sum=0}}{{sum+=$5}}END{{print "
                                           "sum}}'".format('clk', 'dtss-platform-clk'))
        lags['dtss_realtime_base'] = cmdout("kafka-consumer-groups.sh --bootstrap-server 172.28.9.1:9092 --group "
                                           "{} --describe | grep {} | awk 'BEGIN{{sum=0}}{{"
                                           "sum+=$5}}END{{print sum}}'".format('base', 'dtss-realtime-base'))
        lags['dtss_stats_cvt'] = cmdout("kafka-consumer-groups.sh --bootstrap-server 172.28.9.1:9092 --group "
                                           "{} --describe | grep {} | awk 'BEGIN{{sum=0}}{{"
                                           "sum+=$5}}END{{print sum}}'".format('cvt', 'dtss-stats-cvt'))
        lags['dtss_stats_cvt_my'] = cmdout("kafka-consumer-groups.sh --bootstrap-server 172.28.9.1:9092 --group "
                                           "{} --describe | grep {} | awk 'BEGIN{{sum=0}}{{"
                                           "sum+=$5}}END{{print sum}}'".format('my', 'dtss-stats-cvt'))
        lags['dtss_realtime_account'] = cmdout("kafka-consumer-groups.sh --bootstrap-server 172.28.9.1:9092 --group "
                                           "{} --describe | grep {} | awk 'BEGIN{{sum=0}}{{"
                                           "sum+=$5}}END{{print sum}}'".format('account', 'dtss-realtime-account'))
        for key in lags:
          # __init__(self, name, documentation, value=None, labels=None, unit=''):
            lags_gauges[key] = GaugeMetricFamily('td_{}'.format(key), 'metric of {}'.format(key), value=None, labels=['proj', 'service'])
            lags_gauges[key].add_metric(['td', 'kafka'], lags[key])
        for metric in lags_gauges:
            yield lags_gauges[metric]


if __name__ == '__main__':
    start_http_server(23333)
    REGISTRY.register(lagCollector())

    while True:
        time.sleep(10)
