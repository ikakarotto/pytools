#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json

def getTodayPrice():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36",
        "Referer": "http://cn.chowsangsang.com/",
        "Host": "cn.chowsangsang.com"
        }
    url = 'http://cn.chowsangsang.com/script/api/crm/getGoldPrices.php?country=cn'
    response = requests.get(url, headers = headers)
    response.encoding = 'utf-8'
    html = response.text
    for ratedata in json.loads(html)['goldRates']:
        if ratedata['type'] == 'G_JW_SELL':
            return int(ratedata['ptRate']),ratedata['entryDate']

def writelog(filename,content):
    with open(filename, 'a+') as f:
        f.write(content)
    f.close()

if __name__ == '__main__':
    todayprice = getTodayPrice()
    content = "%s | %d\n" % (todayprice[1], todayprice[0])
    print(content)
    logfile = '/data/logs/chowsangsangprice.log'
    writelog(logfile, content)
