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


class offsetsCollector(object):
    def collect(self):
        offsets, offsets_gauges = {}, {}
# [root@emr-worker-1 ~]# kafka-run-class.sh kafka.tools.GetOffsetShell --broker-list 172.28.9.1:9092 --topic dtss-dcs-clk
# dtss-dcs-clk:2:57735119
# dtss-dcs-clk:1:118605963
# dtss-dcs-clk:0:43710137
        # 'dtss-platform-clk', 'dtss-realtime-base', 'dtss-stats-cvt', 'dtss-realtime-account'
        # mysql -h 172.28.26.108 -u readonly -P 3306 -pxxx -e "select sum(line_offset) from alphadesk.report_realtime_consume_offset  where line_consumer ='td-realtime-account' " > rs.out; sed -n "2p" rs.out
        offsets['kafka_offset_account'] = float(cmdout('''
        kafka-run-class.sh kafka.tools.GetOffsetShell --broker-list 172.28.9.1:9092 --topic  dtss-realtime-account  -time -1 ｜ grep dtss-realtime-account | awk -F : '{print $3}' | awk '{sum += $1} END {print sum}'
        '''))
        offsets['kafka_offset_base'] = float(cmdout('''
        kafka-run-class.sh kafka.tools.GetOffsetShell --broker-list 172.28.9.1:9092 --topic  dtss-realtime-base  -time -1 ｜ grep dtss-realtime-base | awk -F : '{print $3}' | awk '{sum += $1} END {print sum}'
        '''))
        for key in offsets:
            offsets_gauges[key] = GaugeMetricFamily('td_kafka_{}'.format(key), 'td_kafka_{}'.format(key), value=offsets[key])
        for metric in offsets_gauges:
            yield offsets_gauges[metric]


if __name__ == '__main__':
    start_http_server(23336)
    REGISTRY.register(offsetsCollector())

    while True:
        time.sleep(10)
