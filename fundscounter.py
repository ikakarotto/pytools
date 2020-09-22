#!/usr/bin/env python3
# coding: utf-8
# 计算 广发多元新兴股票(003745) 净值

import requests
import re
from bs4 import BeautifulSoup
from random import choice

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
    url = 'http://quotes.money.163.com/fund/jzzs_003745.html?start=2020-01-01&end=2020-09-21&order=asc'
    headers ={ 'User-Agent': getRandomUserAgent() }
    value = 1
    
    value = counterNav(value, url)

    next_page = getNextPage(url)
    while next_page:
        url = next_page
        value = counterNav(value, url)
        next_page = getNextPage(url)

