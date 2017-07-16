#!/usr/local/env python
#coding=utf8
__author__ = 'Jiang'


import json

def parse(s):
    """
    parse response,then get market value field
    0:上证(1)/深市(2)
    1：股票代码
    3: 今开
    4:昨收
    7：最低
    11：最高
    31：成交量
    35:成交额：
    37：换手率


    45：流通市值
    46:总市值

    :param s:
    :return:
    """
    d = {}
    values = s[28:-1]
    j = json.loads(values)
    vals = j.get('Value')
    if len(vals) == 0:
        return None
    d['stockid'] = vals[1]
    d['market_start_value'] = vals[3]
    d['lowest_price'] = vals[7]
    d['highest_price'] = vals[11]
    d['deal_mount'] = vals[31]
    d['deal_money'] = vals[35]
    d['change'] = vals[37]
    d['flow_market_value'] = vals[45]
    d['total_market_value'] = vals[46]
    d['date'] = vals[49]
    return d


if __name__ == '__main__':
    d = parse('callback0019589833173166094({"Comment":[],"Value":["2","000651","格力电器","41.08","41.07","41.06","41.05","41.04","41.09","41.10","41.11","41.12","41.13","1081","317","986","562","140","291","1341","201","183","250","0.00","36.91","41.08","40.87","0.07","40.82","0.17","41.33","441473","40.40","5500","41.01","18.0亿","0.54","0.74","15.39","223414","218060","15.32","820","5.25","1","245272361468","247126235483","0|0|0|0|0","0|0|0|0|0","2017-07-14 15:32:28","2.27","-","-"]})')
    print d
