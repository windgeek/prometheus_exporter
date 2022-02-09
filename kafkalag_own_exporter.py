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


class offsetsCollector(object):
    def collect(self):
        offsets, offsets_gauges = {}, {}
        # 'dtss-platform-clk', 'dtss-realtime-base', 'dtss-stats-cvt', 'dtss-realtime-account'
        # mysql -h 172.28.26.108 -u readonly -P 3306 -pxxx -e "select sum(line_offset) from alphadesk.report_realtime_consume_offset  where line_consumer ='td-realtime-account' " > rs.out; sed -n "2p" rs.out
        offsets['kafka_offset_realtime_account'] = float(cmdout('''
        kafka-run-class.sh kafka.tools.GetOffsetShell --broker-list 172.28.9.1:9092 --topic  dtss-realtime-account  -time -1 ｜ grep dtss-realtime-account | awk -F : '{print $3}' | awk '{sum += $1} END {print sum}'
        '''))
        offsets['kafka_offset_realtime_base'] = float(cmdout('''
        kafka-run-class.sh kafka.tools.GetOffsetShell --broker-list 172.28.9.1:9092 --topic  dtss-realtime-base  -time -1 ｜ grep dtss-realtime-base | awk -F : '{print $3}' | awk '{sum += $1} END {print sum}'
        '''))
        offsets['kafka_offset_realtime_cvt'] = float(cmdout('''
        kafka-run-class.sh kafka.tools.GetOffsetShell --broker-list 172.28.9.1:9092 --topic  unique-dtss-stats-cvt  -time -1 ｜ grep unique-dtss-stats-cvt | awk -F : '{print $3}' | awk '{sum += $1} END {print sum}'
        '''))
        offsets['kafka_offset_dcs_clk'] = float(cmdout('''
        kafka-run-class.sh kafka.tools.GetOffsetShell --broker-list 172.28.9.1:9092 --topic  dtss-dcs-clk -time -1 ｜ grep dtss-dcs-clk | awk -F : '{print $3}' | awk '{sum += $1} END {print sum}'
        '''))
        offsets['dtss_realtime_material'] = float(cmdout('''
        kafka-run-class.sh kafka.tools.GetOffsetShell --broker-list 172.28.9.1:9092 --topic  dtss-realtime-material -time -1 ｜ grep dtss-realtime-material | awk -F : '{print $3}' | awk '{sum += $1} END {print sum}'
        '''))
        offsets['dtss_realtime_lineitem'] = float(cmdout('''
        kafka-run-class.sh kafka.tools.GetOffsetShell --broker-list 172.28.9.1:9092 --topic  dtss-realtime-lineitem -time -1 ｜ grep dtss-realtime-lineitem | awk -F : '{print $3}' | awk '{sum += $1} END {print sum}'
        '''))
        #
        # offsets['kafka_offset_realtime_cvt'] = float(cmdout('''
        # mysql -h 172.28.26.108 -u readonly -P 3306 -pxxx -e "select sum(line_offset) from alphadesk.report_realtime_consume_offset  where line_consumer ='td-realtime-cvt' " > cvt.out; sed -n "2p" cvt.out
        # '''))
        # polardb
        offsets['polardb_offset_realtime_account'] = float(cmdout('''
        mysql -h 172.28.26.108 -u readonly -P 3306 -pxxx -e "select sum(line_offset) from alphadesk.report_realtime_consume_offset  where line_consumer ='td-realtime-account' " > account.out; sed -n "2p" account.out
        '''))
        offsets['polardb_offset_realtime_base'] = float(cmdout('''
        mysql -h 172.28.26.108 -u readonly -P 3306 -pxxx -e "select sum(line_offset) from alphadesk.report_realtime_consume_offset  where line_consumer ='td-realtime-base' " > base.out; sed -n "2p" base.out
        '''))
        offsets['polardb_offset_realtime_cvt'] = float(cmdout('''
        mysql -h 172.28.26.108 -u readonly -P 3306 -pxxx -e "select sum(line_offset) from alphadesk.report_realtime_consume_offset  where line_consumer ='td-realtime-cvt' " > cvt.out; sed -n "2p" cvt.out
        '''))
        offsets['polardb_offset_dcs_clk'] = float(cmdout('''
        mysql -h 172.28.26.108 -u readonly -P 3306 -pxxx -e "select sum(line_offset) from alphadesk.report_realtime_consume_offset  where line_consumer ='td-dtss-dcs-clk' " > cvt.out; sed -n "2p" cvt.out
        '''))
        offsets['polardb_offset_realtime_material'] = float(cmdout('''
        mysql -h 172.28.26.108 -u readonly -P 3306 -pxxx -e "select sum(line_offset) from alphadesk.report_realtime_consume_offset  where line_consumer ='td-realtime-material' " > cvt.out; sed -n "2p" cvt.out
        '''))
        offsets['polardb_offset_realtime_materialtag'] = float(cmdout('''
        mysql -h 172.28.26.108 -u readonly -P 3306 -pxxx -e "select sum(line_offset) from alphadesk.report_realtime_consume_offset  where line_consumer ='td-realtime-materialTag' " > cvt.out; sed -n "2p" cvt.out
        '''))
        offsets['polardb_offset_realtime_lineitem'] = float(cmdout('''
        mysql -h 172.28.26.108 -u readonly -P 3306 -pxxx -e "select sum(line_offset) from alphadesk.report_realtime_consume_offset  where line_consumer ='dtss-realtime-lineitem' " > cvt.out; sed -n "2p" cvt.out
        '''))
        for key in offsets:
            offsets_gauges[key] = GaugeMetricFamily('td_{}'.format(key), 'td_{}'.format(key), value=offsets[key])
        for metric in offsets_gauges:
            yield offsets_gauges[metric]


if __name__ == '__main__':
    start_http_server(23339)
    REGISTRY.register(offsetsCollector())

    while True:
        time.sleep(10)

