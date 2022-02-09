#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by wind on 2021/1/19

import subprocess
import pymysql
# ,Summary,Counter,Gauge,Histogram,CollectorRegistry
from prometheus_client import start_http_server
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


def time_create():
    pday = int(time.strftime('%Y%m%d', time.localtime()))
    phour = time.localtime().tm_hour
    # print(phour, type(phour))
    # print(pday, type(pday))
    return pday, phour


def mysql_get(cmd):
    # 打开数据库连接
    db = pymysql.connect(host='172.28.26.108', port=3306, user='readonly', passwd='xxx', db='alphadesk',
                         charset='utf8')
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    # 使用 execute()  方法执行 SQL 查询
    cursor.execute(cmd)
    # 使用 fetchone() 方法获取单条数据.
    data = cursor.fetchone()
    # print(data, type(data))
    # 关闭数据库连接
    db.close()
    return data


def dictpro(names, values):
    nvs = zip(names, values)
    nvDict = dict((name, value) for name, value in nvs)
    return nvDict


class dataCollector(object):
    def collect(self):
        data_gauges = {}
        account_keys = ["td_account_cost", "td_account_imp", "td_account_click", "td_account_activation", "td_account_register", "td_account_conversion", "td_account_retention",
                        "td_account_download_completed", "td_account_awaken", "td_account_media_kuaishou_aclick", "td_account_media_kuaishou_bclick", "td_account_form", "td_account_adv_form", "td_account_adv_valid_clue"]
        account_value = list(mysql_get('''
        select SUM(cost) as td_account_cost , SUM(imp) as td_account_imp, SUM(click) as td_account_click, SUM(activation) as td_account_activation, SUM(register) as td_account_register , SUM(conversion) as td_account_conversion , SUM(retention) as td_account_retention, SUM(download_completed) as td_account_download_completed, SUM(awaken) as td_account_awaken, SUM(media_kuaishou_aclick) as td_account_media_kuaishou_aclick, SUM(media_kuaishou_bclick) as td_account_media_kuaishou_bclick, sum(form) as td_account_form, sum(adv_form) as td_account_adv_form, SUM(adv_valid_clue) as td_account_adv_valid_clue from alphadesk.report_realtime_account where pday=date_format(now(),'%Y%m%d');'''))
        creative_kyes = ["td_creative_cost",  "td_creative_imp",  "td_creative_click",  "td_creative_activation",  "td_creative_register",  "td_creative_conversion",  "td_creative_retention",  "td_creative_download_completed",
                         "td_creative_awaken",  "td_creative_media_kuaishou_aclick",  "td_creative_media_kuaishou_bclick",  "td_creative_form",  "td_creative_adv_form",  "td_creative_adv_valid_clue", "td_creative_drs_click"]
        creative_value = list(mysql_get('''
        select SUM(cost) as td_creative_cost , SUM(imp) as td_creative_imp, SUM(click) as td_creative_click, SUM(activation) as td_creative_activation, SUM(register) as td_creative_register , SUM(conversion) as td_creative_conversion , SUM(retention) as td_creative_retention, SUM(download_completed) as td_creative_download_completed, SUM(awaken) as td_creative_awaken, SUM(media_kuaishou_aclick) as td_creative_media_kuaishou_aclick, SUM(media_kuaishou_bclick) as td_creative_media_kuaishou_bclick, sum(form) as td_creative_form, sum(adv_form) as td_creative_adv_form, SUM(adv_valid_clue) as td_creative_adv_valid_clue,  SUM(drs_click) as td_creative_drs_click from alphadesk.report_realtime_creative where pday=date_format(now(),'%Y%m%d');'''))
        account_dict = dictpro(account_keys, account_value)
        creative_dict = dictpro(creative_kyes, creative_value)
        pday, phour = time_create()
        hour_account_keys = ['hour_account_imp',
                             'hour_account_cost', 'hour_account_clk']
        hour_account_value = list(mysql_get('''
        select SUM(imp) as hour_account_imp,sum(cost) as hour_account_cost,SUM(click) as hour_account_clk from alphadesk.report_realtime_account where pday={} and phour={};
        '''.format(pday, phour)))
        hour_account_dict = dictpro(hour_account_keys, hour_account_value)
        hour_creative_keys = ['hour_creative_imp',
                              'hour_creative_cost', 'hour_creative_clk', 'hour_creative_drs_click']
        hour_creative_value = list(mysql_get('''
        select SUM(imp) as hour_creative_imp,sum(cost) as hour_creative_cost,SUM(click) as hour_creative_clk, SUM(drs_click) as hour_creative_drs_click from alphadesk.report_realtime_creative where pday={} and phour={};
        '''.format(pday, phour)))
        hour_creative_dict = dictpro(hour_creative_keys, hour_creative_value)
        for key in account_dict:
            data_gauges[key] = GaugeMetricFamily('polardb_{}'.format(
                key), 'td_polardb', value=account_dict[key])
        for key in creative_dict:
            data_gauges[key] = GaugeMetricFamily('polardb_{}'.format(
                key), 'td_polardb', value=creative_dict[key])
        for key in hour_account_dict:
            data_gauges[key] = GaugeMetricFamily('polardb_{}'.format(
                key), 'td_polardb', value=hour_account_dict[key])
        for key in hour_creative_dict:
            data_gauges[key] = GaugeMetricFamily('polardb_{}'.format(
                key), 'td_polardb', value=hour_creative_dict[key])
        for metric in data_gauges:
            yield data_gauges[metric]


if __name__ == '__main__':
    start_http_server(23337)
    REGISTRY.register(dataCollector())

    while True:
        time.sleep(10)


# select SUM(cost) as td_creative_cost , SUM(imp) as td_creative_imp, SUM(click) as td_creative_click, SUM(activation) as td_creative_activation, SUM(register) as td_creative_register , SUM(conversion) as td_creative_conversion , SUM(retention) as td_creative_retention, SUM(download_completed) as td_creative_download_completed, SUM(awaken) as td_creative_awaken, SUM(media_kuaishou_aclick) as td_creative_media_kuaishou_aclick, SUM(media_kuaishou_bclick) as td_creative_media_kuaishou_bclick, sum(form) as td_creative_form, sum(adv_form) as td_creative_adv_form, SUM(adv_valid_clue) as td_creative_adv_valid_clue sum(drs_click) as td_creative_drs from alphadesk.report_realtime_creative where pday=date_format(now(),'%Y%m%d');'''))
