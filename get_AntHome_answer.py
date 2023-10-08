#!/usr/bin/env python3
# coding: utf-8

import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime,timedelta
from pprint import pprint

def get_answer1():
    headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
            "Referer": "http://www.xuexili.com/"
            }
    url = 'http://www.xuexili.com/mayizhuangyuan/jinridaan.html'
    try:
        response = requests.get(url, headers=headers)
        response.encoding = 'utf-8'
        html = response.text
        #print(html)
        soup = BeautifulSoup(html, 'lxml')
        tables = soup.find_all('table', {'border': '1', 'cellpadding': '1', 'cellspacing': '1', 'style': 'width: 98%'})
        trs = tables[0].find_all('tr')
        tr = trs[1]
        print(tr.text.split())

    except Exception as e:
        raise e


def get_answer_from_index(url):
    date_now = datetime.now().strftime('%Y-%m-%d')
    date_yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
            "Referer": "http://www.mnw.cn/"
            }
    try:
        response = requests.get(url, headers=headers)
        response.encoding = 'utf-8'
        html = response.text
        soup = BeautifulSoup(html, 'lxml')
        dds = soup.find_all('dd', {'class': 'list3'})
        for dd in dds:
            for div in dd.find_all('div',{'class': ''}):
                tag_a = div.find('a', href=True)
                href = tag_a['href']
                title = tag_a.text
                if '蚂蚁庄园' in title:
                    tag_span = div.find('span')
                    span_text = tag_span.text
                    article_time = ' '.join(span_text.split()[:2])
                    for date in (date_now,date_yesterday):
                        if date in article_time:
                            title = title.replace('今日蚂蚁庄园小鸡课堂正确答案最新：','')
                            titles = re.findall(r'(.*?？)', title)
                            titles = [title if not titles else titles]
                            #print(href,titles,article_time)
                            #print(titles,article_time)
                            results = get_answer_from_url(href)
                            print(article_time)
                            print(list(zip(titles,results)))
    except Exception as e:
        raise e

def get_answer_from_url(url):
    date_now = datetime.now().strftime('%Y-%m-%d')
    date_yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    #url = 'http://www.mnw.cn/keji/internet/2818884.html'
    headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
            "Referer": "http://www.mnw.cn/"
            }
    try:
        response = requests.get(url, headers=headers)
        response.encoding = 'utf-8'
        html = response.text
        soup = BeautifulSoup(html, 'lxml')
        divs = soup.find_all('div', {'class': 'icontent'})
        for div in divs:
            #print(div.text)
            #pprint(div.text.strip().split('\u3000\u3000'))
            data = re.findall(r'<\/?strong>答案：(.*?)<\/strong>|<\/?strong>　+答案：(.*?)<\/strong>|<\/?strong>　　正确答案：(.*?)<\/strong>', str(div))
            result = [subitem for item in data for subitem in item if subitem]
            return result
    except Exception as e:
        raise e

if __name__ == '__main__':
    get_answer1()
    get_answer_from_index('http://www.mnw.cn/keji/internet/')
    get_answer_from_index('http://www.mnw.cn/keji/mi/')
    




