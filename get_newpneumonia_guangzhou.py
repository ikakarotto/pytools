#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Description: 获取广州卫健委疫情通报情况

import time
import random
import re
import urllib.request
from bs4 import BeautifulSoup

# 获取分页的url地址
def get_next_page(urls):
    url = urls[-1]
    request=urllib.request.Request(url,headers=headers)
    response=urllib.request.urlopen(request).read()
    response = response.decode("UTF-8")
    try:
        next_url = re.findall(r'<a class="next" href="(.*)">', response)[0]
        if next_url:
            urls.append(next_url)
            get_next_page(urls)
    except:
        pass
    return urls

# 获取当前页的新闻url以及标题
def get_days_url(url):
    time.sleep(random.choice(range(1,11)))
    request=urllib.request.Request(url,headers=headers)
    response=urllib.request.urlopen(request).read()
    response = response.decode("UTF-8")
    attrnews = re.findall(r'<a href="(http://wjw.gz.gov.cn/ztzl/.*)" target="_blank" title="(.*)">.*',response)
    return attrnews

# 获取指定url中的疫情通报情况
def get_day_news(url):
    time.sleep(random.choice(range(1,11)))
    request=urllib.request.Request(url,headers=headers)
    response=urllib.request.urlopen(request).read()
    response = response.decode("UTF-8")
    m = re.search(r'(<p indenttext=".*</p>|<p style.*</p>)|<p><span style.*</span></p>', response, flags=re.I)
    news = m.group()
    data = BeautifulSoup(news, "lxml").text
    return data


if __name__ == '__main__':
    urls = ['http://wjw.gz.gov.cn/ztzl/xxfyyqfk/yqtb/index.html']
    headers ={
       'User-Agent':'Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    for page_url in get_next_page(urls):
        for dayinfo in get_days_url(page_url):
            dayurl = dayinfo[0]
            daytitle = dayinfo[1]
            print('============================' + daytitle + '============================')
            daydata = get_day_news(dayurl)
            for i in daydata.split('\u3000\u3000'):
                print(i)
            print()
