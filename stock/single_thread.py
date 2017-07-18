#!/usr/bin/env python
#coding=utf8

import sys
import time
import logging
import datetime

import requests
import pymysql

import parse_resp
from dbsettings import dbparam



## generate url
def generate_url(stockid):
    url = 'http://nuff.eastmoney.com/EM_Finance2015TradeInterface/JS.ashx?id={}{}&token=beb0a0047196124721f56b0f0ff5a27c\
&cb=callback0019589833173166094&callback=callback0019589833173166094'
    if stockid.startswith('6'):
        url = url.format(stockid, 1)
    elif stockid.startswith(('0','3')):
        url = url.format(stockid, 2)
    else:
        return None
    return url


def get_stock_info(stockid):
    url = generate_url(stockid)
    if url is None:
        return None
    resp = requests.get(url)
    if resp.status_code == 200:
        resp.encoding = 'gbk'
        content = resp.content
        res = parse_resp.parse(content)
        return res
    else:
        return None


def get_all_info():
    errfile = 'err.log'
    ferr = open('err.log','a')
    #1、连接数据库
    conn = pymysql.connect(**dbparam)
    if not conn:
        print '数据库连接错误'
        sys.exit(-1)

    cursor = conn.cursor()
    sql = 'select stockid from stocks'
    allstocksid = cursor.execute(sql)
    count = 0
    for item in cursor.fetchall():
        try:
            stockid = item[0]
            res = get_stock_info(stockid)
            if res is not None:
                count += 1
                #把数据写入数据库
                sql = u"insert into dayinfo(stockid, today_start_price,lowest_price,\
hight_price,deal_mount,deal_money,exchange,\
flow_market_value,total_market_value,info_date, zhangfu)\
values('{}',{},{},{},{},'{}',{},{},{},'{}',{})".format(\
res['stockid'],float(res['market_start_value']),float(res['lowest_price']),res['highest_price'],\
res['deal_mount'],res['deal_money'],res['change'],res['flow_market_value'],res['total_market_value'],\
res['date'][:10], res['zhangfu'])
            cursor.execute(sql.encode('utf8'))
            if count % 10 == 0:
                conn.commit()
            time.sleep(0.1)
        except Exception, e:
            ferr.write(sql.encode('utf8') + '\n')
	    ferr.write(e + '\n')
    conn.commit()
    ferr.close()
    cursor.close()
    conn.close()


if __name__ == '__main__':
	
   d = datetime.datetime.now()
   start_time = d.strftime('%Y-%m-%d %H:%M:%S')
   get_all_info()
   d2 = datetime.datetime.now()
   end_time = d2.strftime('%Y-%m-%d %H:%M:%S')
   with open('crawler.log', 'a') as f:
	   f.write('Start at' + start_time + ' and finished at ' + end_time + '\n')
