#!/usr/bin/env python3
# coding: utf-8
# --------- 爬虫写得好，牢饭包管饱 ---------
# 计算基金净值
# python3 fundscounter.py
# python3 fundscounter.py 164701
# python3 fundscounter.py 164701 2020-07-01
# fundcode = 164701 # 汇添富黄金及贵金属(164701)

import requests
import re
from bs4 import BeautifulSoup
from random import choice
import sys
import datetime
import time

# 随机获取UserAgent
def getRandomUserAgent():
    # https://www.whatismybrowser.com/guides/the-latest-user-agent/chrome
    # https://github.com/fengzhizi715/user-agent-list
    # https://deviceatlas.com/blog/list-of-user-agent-strings
    # https://developers.whatismybrowser.com/api/docs/latest/user-agent-database-dump-url-txt-sample.tar.gz

    agents = [
                 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
                 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
                 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
                 'Mozilla/5.0 (Linux; Android 8.0.0;) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.93 Mobile Safari/537.36',
                 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/79.0.3945.73 Mobile/15E148 Safari/605.1',
                 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0',
                 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:61.0) Gecko/20100101 Firefox/71.0',
                 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
                 'Mozilla/5.0 (Linux; Android 8.0.0; SM-G960F Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.84 Mobile Safari/537.36'
        ]
    return choice(agents)

# 获取基金净值页面标题
def getTitle(url):
    response = requests.get(url, headers = headers)
    response.encoding = 'utf-8'
    html = response.text

    h2 = re.findall(r'(<h2>.*?净值走势</h2>)', html)[0]
    h2Obj = BeautifulSoup(h2, 'lxml')
    print(h2Obj.text)

# 获取下一页链接
def getNextPage(url):
    response = requests.get(url, headers = headers)
    response.encoding = 'utf-8'
    html = response.text
    
    mod_pages = re.findall(r'(<div class="mod_pages">.*?</div>)', html, flags=re.DOTALL)[0]
    modObj = BeautifulSoup(mod_pages, 'lxml')
    tags = modObj.findAll('a')
    for tag in tags:
        if tag.get_text() == '下一页':
            next_page = 'http://quotes.money.163.com' + tag.attrs.get('href')
            next_page = next_page.replace('&order=desc','&order=asc')
            return next_page

# 统计净值
def counterNav(value, url):
    response = requests.get(url, headers = headers)
    response.encoding = 'utf-8'
    html = response.text

    tbody = re.findall(r'(<tbody>.*?</tbody>)', html, flags=re.DOTALL)[0]
    bsObj = BeautifulSoup(tbody, 'lxml')
    list_tr = bsObj.findAll(name = 'tr')

    for tr in list_tr:
        trvars = re.split('\n+', tr.text)
        trvars = list(filter(None, trvars))
        [date, nav, nav1, avg] = trvars
        avgf = float(avg.replace('%',''))
        value = value*(100+avgf)/100
        # print(date,avgf)
        print(date,value)
    return value


if __name__ == '__main__':
    if len(sys.argv) > 1:
        fundcode = sys.argv[1]
        if len(sys.argv) > 2:
            datestart = sys.argv[2]
        else:
            datestart = '2020-01-01'
    else:
        fundcode = 164701 # 汇添富黄金及贵金属(164701)
        datestart = '2020-01-01'

    # 前一天的日期
    dateend = datetime.date.today() + datetime.timedelta(-1)
    dateend = dateend.strftime('%Y-%m-%d')

    # 
    # dateyes = datetime.date.today() + datetime.timedelta(-1)
    # dateyes = dateyes.strftime('%Y-%m-%d')
    # datecount = 31
    # datebef31 = datetime.date.today() + datetime.timedelta(-datecount)
    # datebef31 = datebef31.strftime('%Y-%m-%d')

    # 拼接基金净值地址
    # url = 'http://quotes.money.163.com/fund/jzzs_164701.html?start=2020-01-01&end=2020-09-21&order=asc'
    url = 'http://quotes.money.163.com/fund/jzzs_' + str(fundcode) + '.html?start=' + datestart + '&end=' + dateend + '&order=asc'

    headers ={ 'User-Agent': getRandomUserAgent() }
    getTitle(url)
    # 定义净值基数为1
    valueint = 1
    # 计算第一页的基金净值
    value = counterNav(valueint, url)

    # 获取下一页的基金净值
    next_page = getNextPage(url)
    while next_page:
        time.sleep(random.choice(range(1,11)))
        url = next_page
        value = counterNav(value, url)
        next_page = getNextPage(url)

    print('%.2f' % ((value-valueint)/valueint*100))
