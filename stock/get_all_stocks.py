#!/usr/bin/env python
#coding=utf8
# 获取所有股票的代码，并存到文件或者数据库中
# Date : 2017-7-9


import sys
import re

import requests

import pymysql

from dbsettings import dbparam

url = 'http://quote.eastmoney.com/stocklist.html'
res = requests.get(url)
res.encoding = 'gbk'
#print res.text
#正则查找股票代码
#//*[@id="quotesearch"]/ul[2]/li[51]/a
t = '<a target="_blank" href="http://quote.eastmoney.com/sz000058.html">深赛格(000058)</a>'
pattern = r'<a target="_blank" href="http://quote.eastmoney.com/s[z|h)](\d+?).html">(.*?)\(\1\)</a>'

m = re.findall(pattern, res.text)

#for item in m:
#    if item[0].startswith(('3','6','0')):
#        print item[0], item[1]


# 1连接数据库


conn = pymysql.connect(**dbparam)
if not conn:
    print '数据库连接错误'
    sys.exit(-1)

cursor = conn.cursor()
#cursor.execute('select count(*) from stocks')
#print cursor.fetchone()
sql = u'insert into stocks(stockid, name) values '
for item in m:
    if item[0].startswith(('3','6','0')):
        s = u"('{}','{}'),".format(item[0],item[1])
        sql += s
sql = sql.strip(',')
r = cursor.execute(sql.encode('utf8'))
print r
if r > 0:
    conn.commit()
cursor.close()
conn.close()