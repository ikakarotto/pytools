#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import requests
import re
import json
import time
from bs4 import BeautifulSoup
from pyquery import PyQuery as pq
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

# 获取页面标题
def getTitle(url):
#    response = pq(url=url, headers = headers)
#    return response('title').text()
    response = requests.get(url, headers = headers)
    response.encoding = 'utf-8'
    # soup = BeautifulSoup(response.text, 'lxml')
    # return soup.find('title').text.strip()
    html = response.text
    title = ''
    title_list = re.findall(r'<meta property="og:title" content="(.*?)" />|<title>(\n?.*?)</title>', html)
    # print(title_list)
    # print(html)
    for i in title_list[0]:
         if i: title = i.strip().replace(' - FreeBuf网络安全行业门户','')
    return title

# 获取最新的早报链接
def getFreebufLatestLink():
    '''
    time_date = time.strftime('%Y-%m-%d', time.localtime())
    url = 'https://www.freebuf.com/news'
    link = ''
    response = requests.get(url, headers = headers)
    response.encoding = 'utf-8'
    html = response.text
    bsObj = BeautifulSoup(html, 'lxml')
    list_dl = bsObj.findAll(name = 'dl')
    for dl in list_dl:
        if '早报' in dl.text and time_date in dl.text:
            news_time = dl.find('span', class_="time").get_text().strip()
            if news_time == time_date:
                # title = dl.find('a', class_='article-title').get_text().strip()
                link = dl.find('a', {"target":"_blank"}).attrs['href']
                # print(news_time)
                # print(title)
                # print(link)
    return link
    '''

    time_date = time.strftime('%Y-%m-%d', time.localtime())
    url = 'https://www.freebuf.com/news'
    link = ''
    response = requests.get(url, headers = headers)
    response.encoding = 'utf-8'
    html = response.text
    bsObj = BeautifulSoup(html, 'lxml')
    list_tag_a = bsObj.findAll(name = 'a')
    for tag_a in list_tag_a:
        if '早报' in tag_a.text:
            title = tag_a.text
            url = tag_a.attrs['href']
            if url.startswith('/'): url = 'https://www.freebuf.com' + url
            break

    return url

# 发送到钉钉
def sendNewsToDtalk(links):
    headers['Content-Type'] = 'application/json'
    parameter = {
        "feedCard": {
            "links": links
        }, 
        "msgtype": "feedCard"
    }

    request = requests.post(dtalk_robot, data=json.dumps(parameter), headers=headers)
    # return request.text

# 获取图片地址, 用于钉钉通知的feedCard背景
def getImgList():
    urls = [
           'https://www.2717.com/zt/maomi/1/',
           'https://www.2717.com/zt/maomi/2/',
           'https://www.2717.com/zt/maomi/3/'
           ]
    imgurls = []
    for url in urls:
        response = requests.get(url, headers = headers)
        response.encoding = 'utf-8'
        html = response.text
        bsObj = BeautifulSoup(html, 'lxml')
        for ul in bsObj.findAll('ul', {"id":"ImagesLoad1"}):
            imglist = ul.select('img')
            for img in imglist:
                # print(img)
                imgurls.append(img.attrs['src'])

    picurls = [
              'http://inews.gtimg.com/newsapp_bt/0/10930597635/1000.jpg',
              'http://pic2.zhimg.com/50/v2-3ef8a0be30fcd1dc63218600e339bcb9_hd.jpg',
              'https://pic1.zhimg.com/80/v2-5616e373076a5948814ce75a86346a21_hd.jpg',
              'http://bpic.588ku.com/element_origin_min_pic/01/38/26/95573c7bda89ea3.jpg',
              'https://pic1.zhimg.com/80/v2-5b8b3cf68a1efb67b963f944838bd2e1_hd.jpg',
              'https://pic2.zhimg.com/80/v2-000bddba9ed217c2b81d907ef1ea81fa_hd.jpg',
              'https://pic2.zhimg.com/80/v2-692720a1fa05637db980d42dbd7df14a_hd.jpg',
              'https://pic3.zhimg.com/80/v2-fdf57d2ac2bca4903b9e43a9f30b1860_hd.jpg',
              'https://pic2.zhimg.com/80/v2-ed7574220e9bc61073f5c116701907a9_hd.jpg',
              'https://pic4.zhimg.com/80/v2-2b7757d3161bf5a84bc1c0ff3ae46bc4_hd.jpg',
              'https://pic4.zhimg.com/80/v2-b4b51bbff65fcb3e3ebae358eca7fa32_hd.jpg',
              'https://pic3.zhimg.com/80/v2-c63b70e7a5b1de1bb50be73f8f32d2d4_hd.jpg',
              'https://pic2.zhimg.com/80/v2-067d202c45597c38f53639a96ccba191_hd.jpg',
              'https://pic4.zhimg.com/80/v2-ee571d63afe6fdffe5cc77bf974bbcc9_hd.jpg',
              'https://pic3.zhimg.com/80/v2-45ac3f41f98e45467aa1aed22dbd4836_hd.jpg',
              'https://pic2.zhimg.com/80/v2-fa1bf84a90bcc3caee3964dc984a360e_hd.jpg'
    ]

    imgurls += picurls
    return imgurls


if __name__ == '__main__':
    # dtalk_robot = 'https://oapi.dingtalk.com/robot/send?access_token=3cf6cafccae6017f24d038d3b3fe732b7d9aa2c9b6b89c8837f8ee3ee17eed98'
    dtalk_robot = 'https://oapi.dingtalk.com/robot/send?access_token=3b15eedc17a5e896dfdcc2a0ab6b7e1739e1f282849e4eaa24f4a11dd43ae296'
    # dtalk_robot = 'https://oapi.dingtalk.com/robot/send?access_token=19646e4e77da1ab6fc51f41026bcecd7ef6d01ca12333b305676bdfdedb52818'
    headers ={ 'User-Agent': getRandomUserAgent() }

    picurls = getImgList()

    links = []

    for inputurl in sys.argv[1:]:
        if inputurl.startswith('http://') or inputurl.startswith('https://'):
            title = getTitle(inputurl)
            inputurl = inputurl.replace('www.freebuf','m.freebuf')
            if title:
                links.append({"title": title, "messageURL": inputurl, "picURL": choice(picurls)})

        elif inputurl == 'latest':
            url_freebuf_latest = getFreebufLatestLink()
            if url_freebuf_latest:
                title = getTitle(url_freebuf_latest)
                url_freebuf_latest = url_freebuf_latest.replace('www.freebuf','m.freebuf')
                if title:
                    links.append({"title": title, "messageURL": url_freebuf_latest, "picURL": choice(picurls)})

        else:
            print('URL非法: ' + inputurl)
            sys.exit(1)
    
    if links:
        # print(links)
        # print(sendNewsToDtalk(links))
        sendNewsToDtalk(links)

'''
Reference: https://ding-doc.dingtalk.com/doc#/serverapi2/qf2nxq

https://mp.weixin.qq.com/s/jcCFZb2lJmBOVodH28cKBw https://xz.aliyun.com/t/6902 https://app.myzaker.com/news/article.php?pk=5df11b1e8e9f090f5f1c393a https://threatpost.com/ge-dunkin-forever21-internal-doc-leak/150920/ https://www.freebuf.com/articles/web/222060.html

https://mp.weixin.qq.com/s/jcCFZb2lJmBOVodH28cKBw https://xz.aliyun.com/t/6902 https://app.myzaker.com/news/article.php?pk=5df11b1e8e9f090f5f1c393a https://www.freebuf.com/articles/web/222060.html

python3 get_freebuf_news.py https://xxxxxx
python3 get_freebuf_news.py latest
'''

