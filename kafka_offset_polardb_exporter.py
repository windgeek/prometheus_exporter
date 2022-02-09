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
        # 'dtss-platform-clk', 'dtss-realtime-base', 'dtss-stats-cvt', 'dtss-realtime-account'
        # mysql -h 172.28.26.108 -u readonly -P 3306 -pxxx -e "select sum(line_offset) from alphadesk.report_realtime_consume_offset  where line_consumer ='td-realtime-account' " > rs.out; sed -n "2p" rs.out
        offsets['offset_realtime_account'] = float(cmdout('''
        mysql -h 172.28.26.108 -u readonly -P 3306 -pxxx -e "select sum(line_offset) from alphadesk.report_realtime_consume_offset  where line_consumer ='td-realtime-account' " > account.out; sed -n "2p" account.out
        '''))
        offsets['offset_realtime_base'] = float(cmdout('''
        mysql -h 172.28.26.108 -u readonly -P 3306 -pxxx -e "select sum(line_offset) from alphadesk.report_realtime_consume_offset  where line_consumer ='td-realtime-base' " > base.out; sed -n "2p" base.out
        '''))
        offsets['offset_realtime_cvt'] = float(cmdout('''
        mysql -h 172.28.26.108 -u readonly -P 3306 -pxxx -e "select sum(line_offset) from alphadesk.report_realtime_consume_offset  where line_consumer ='td-realtime-cvt' " > cvt.out; sed -n "2p" cvt.out
        '''))
        for key in offsets:
            offsets_gauges[key] = GaugeMetricFamily('td_polardb_{}'.format(key), 'td_polardb_{}'.format(key), value=offsets[key])
        for metric in offsets_gauges:
            yield offsets_gauges[metric]


if __name__ == '__main__':
    start_http_server(23338)
    REGISTRY.register(offsetsCollector())

    while True:
        time.sleep(10)
