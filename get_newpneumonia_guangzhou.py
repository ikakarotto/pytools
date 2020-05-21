#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Description: 获取广州卫健委疫情通报情况

import re
import urllib.request
from bs4 import BeautifulSoup

# 获取【疫情通报】第一页的url以及标题
def get_days_url(url):
    request=urllib.request.Request(url,headers=headers)
    response=urllib.request.urlopen(request).read()
    response = response.decode("UTF-8")
    attrnews = re.findall(r'<a href="(http://wjw.gz.gov.cn/ztzl/.*)" target="_blank" title="(.*)">.*',response)
    return attrnews

# 获取指定url中的疫情通报情况
def get_day_news(url):
    request=urllib.request.Request(url,headers=headers)
    response=urllib.request.urlopen(request).read()
    response = response.decode("UTF-8")
    m = re.search(r'(<p indenttext=".*</p>|<p style.*</p>)', response, flags=re.I)
    news = m.group()
    data = BeautifulSoup(news, "lxml").text
    return data


if __name__ == '__main__':
    url = 'http://wjw.gz.gov.cn/ztzl/xxfyyqfk/yqtb/index.html'
    headers ={
       'User-Agent':'Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    for dayinfo in get_days_url(url):
        dayurl = dayinfo[0]
        daytitle = dayinfo[1]
        print('============================' + daytitle + '============================')
        daydata = get_day_news(dayurl)
        for i in daydata.split(): print(i)
