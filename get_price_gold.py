#!/usr/bin/env python3
# coding: utf-8

import requests
import time
import datetime
import json
from bs4 import BeautifulSoup
from random import choice
from pprint import pprint

#### get gold code list
def get_gold_list():
    gold_list = []
    headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
            "Referer": "https://quote.cngold.org/"
            }
    url = 'https://quote.cngold.org/gjs/swhj.html'
    try:
        response = requests.get(url, headers=headers)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        divs = soup.find_all('div', class_='shwj_list')
        lis = []
        for div in divs:
            lis += div.find_all('li')
            for li in lis:
                a = li.find('a')
                gold_href = a['href']
                #print(gold_href)
                img = li.find('img')
                gold_name = img['title']
                table = li.find('table')
                for tr in table.find_all('tr'):    #tr = table.find('tr')
                    gold_type = tr.find('td').text
                    td = tr.find_all('td')[1]
                    if 'id' in td.attrs: gold_code = td['id'].replace('_price','')
                    # print(gold_code,gold_name)
                    # print('\n'*3)
                    if gold_type != '----': gold_list.append((gold_name,gold_code,gold_type,gold_href))
        return gold_list
    except Exception as e:
        raise e

def get_gold_price_realtime(gold_array):
    gold_name,gold_code,gold_type,gold_href = gold_array
    date = time.strftime('%Y-%m-%d', time.localtime())
    #### filter some keywords
    for gold_key in ['黄金','金条','足金','基础金价','零售价','回收价']:
        if gold_key in gold_type:
            ts = int(time.time()*1000)
            url = f'https://api.jijinhao.com/quoteCenter/realTime.htm?codes={gold_code}&_={ts}'
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
                "Referer": gold_href
                }
            response = requests.get(url, headers=headers)
            resp = response.text
            try:
                start_index = resp.find('{')
                end_index = resp.rfind('}') + 1
                quote_json = resp[start_index:end_index]
                quote_dict = json.loads(quote_json)
                gold_price = quote_dict[gold_code]['q1'] if len(quote_dict[gold_code]) else "0"
                print(date, gold_name, gold_type, int(gold_price))
            except Exception as e:
                raise e

def get_gold_price_history(date,gold_array):
    gold_name,gold_code,gold_type,gold_href = gold_array
    #### filter some keywords
    for gold_key in ['黄金','金条','足金','基础金价','零售价','回收价']:
        if gold_key in gold_type:
            ts = int(time.time()*1000)
            url = f'https://api.jijinhao.com/quoteCenter/history.htm?code={gold_code}&style=3&pageSize=10&needField=128,129,70&startDate={date}&endDate={date}&_={ts}'
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
                "Referer": gold_href
                }
            response = requests.get(url, headers=headers)
            resp = response.text
            try:
                start_index = resp.find('{')
                end_index = resp.rfind('}') + 1
                quote_json = resp[start_index:end_index]
                quote_dict = json.loads(quote_json)
                gold_price = quote_dict['data'][0]['q1'] if len(quote_dict['data']) else "0"
                print(date, gold_name, gold_type, int(gold_price))
            except Exception as e:
                raise e


if __name__ == '__main__':
    gold_list = get_gold_list()
    # pprint(gold_list)

    #### get realtime price
    for gold_array in gold_list[:40]:
        time.sleep(choice(range(1,21))/10)
        get_gold_price_realtime(gold_array)

    #### get history price
    # date = '2023-02-01'
    # date = time.strftime('%Y-%m-%d', time.localtime())
    date = (datetime.date.today()-datetime.timedelta(days=1)).strftime('%Y-%m-%d')
    for gold_array in gold_list[:40]:
        time.sleep(choice(range(1,21))/10)
        get_gold_price_history(date,gold_array)


'''
https://quote.cngold.org/gjs/swhj.html
https://api.jijinhao.com/quoteCenter/realTime.htm?codes=JO_42660,JO_42661,JO_56037,JO_42657,JO_42658,JO_42659,JO_42653,JO_42654,JO_42656,JO_42625,JO_42626,JO_56045,JO_42646,JO_42647,JO_56041,JO_42638,JO_42639,JO_42643,JO_42632,JO_42633,JO_42668,JO_42634,JO_42635,JO_42636,JO_52670,JO_61954,JO_52678,JO_52677,JO_52672,JO_52671,JO_52674,JO_52673,JO_52676,JO_52675,JO_52680,JO_52679,JO_52683,JO_52684,JO_52685,JO_52681,JO_52682,JO_52686,JO_54155,JO_52689,JO_54372,JO_52692,JO_52693,JO_52694,JO_52695,JO_52696,JO_61908,JO_52698,JO_52699,JO_52700,JO_52702,JO_52701,JO_52703,JO_52705,JO_52704,JO_52707,JO_52706,JO_52709,JO_52708,JO_52711,JO_52712,JO_61906,JO_61905,JO_61428,JO_61429,JO_61435,JO_61434,JO_63849,JO_63851,JO_63850,JO_63852,JO_92438,JO_92441,JO_92439,JO_92440,JO_95167,JO_95168,JO_95169,JO_292800,JO_292801,JO_292802,JO_321446,JO_321448,JO_321450,JO_335546,JO_335545,JO_335547&_=1683195577203
https://api.jijinhao.com/quoteCenter/realTime.htm?codes=JO_42660&_=1683344236026

2023-05-05 周大福 黄金价格 592.0
2023-05-05 周大福 铂金价格 410.0
2023-05-05 周大福 金条金价(内地) 582.0
2023-05-05 老凤祥 黄金价格 593.0
2023-05-05 老凤祥 铂金价格 365.0
2023-05-05 老凤祥 足金价格 593.0
2023-05-05 周六福 黄金价格 593.0
2023-05-05 周六福 铂金价格 433.0
2023-05-05 周六福 金条价格 529.0
2023-05-05 周生生 黄金价格 592.0
2023-05-05 周生生 铂金价格 410.0
2023-05-05 周生生 金条价格(内地) 582.0
2023-05-05 六福珠宝 黄金价格 592.0
2023-05-05 六福珠宝 铂金价格 410.0
2023-05-05 六福珠宝 金条价格(内地) 582.0
2023-05-05 菜百 黄金价格 575.0
2023-05-05 菜百 铂金价格 358.0
2023-05-05 菜百 足金价格 575.0
2023-05-05 金至尊 黄金价格 592.0
2023-05-05 金至尊 铂金价格 410.0
2023-05-05 金至尊 首饰 592.0
2023-05-05 老庙 黄金价格 593.0
2023-05-05 老庙 铂金价格 360.0
2023-05-05 老庙 足金价格 593.0
2023-05-05 潮宏基 黄金价格 592.0
2023-05-05 潮宏基 铂金价格 410.0
2023-05-05 周大生 黄金价格 584.0
2023-05-05 周大生 铂金价格 415.0
2023-05-05 亚一金店 黄金价格 593.0
2023-05-05 亚一金店 铂金价格 360.0
2023-05-05 宝庆银楼 黄金价格 566.0
2023-05-05 宝庆银楼 铂金价格 368.0
2023-05-05 太阳金店 黄金价格 519.0
2023-05-05 太阳金店 铂金价格 369.0
2023-05-05 齐鲁金店 黄金价格 516.0
2023-05-05 齐鲁金店 铂金价格 359.0
2023-05-05 中国黄金 基础金价 455.5
2023-05-05 中国黄金 零售价 469.5
2023-05-05 中国黄金 回收价 453.5
2023-05-05 高赛尔 金条 467.7
2023-05-05 高赛尔 银条 5.59
2023-05-05 千禧之星 黄金价格 593.0
2023-05-05 千禧之星 铂金价格 360.0
2023-05-05 吉盟珠宝 黄金价格 592.0
2023-05-05 吉盟珠宝 铂金价格 410.0
2023-05-05 东祥金店 黄金价格 592.0
2023-05-05 东祥金店 铂金价格 410.0
2023-05-05 萃华金店 黄金价格 508.0
2023-05-05 萃华金店 铂金价格 391.0
2023-05-05 百泰黄金 黄金价格 594.0
2023-05-05 百泰黄金 金条价格 486.0
2023-05-05 金象珠宝 黄金价格 580.0
2023-05-05 常州金店 黄金价格 575.0
2023-05-05 常州金店 铂金价格 395.0
2023-05-05 扬州金店 黄金价格 500.0
2023-05-05 扬州金店 铂金价格 360.0
2023-05-05 嘉华珠宝 黄金价格 592.0
2023-05-05 福泰珠宝 黄金价格 562.0
2023-05-05 福泰珠宝 铂金价格 360.0
2023-05-05 城隍珠宝 黄金价格 583.0
2023-05-05 城隍珠宝 铂金价格 350.0
2023-05-05 星光达珠宝 黄金价格 593.0
2023-05-05 星光达珠宝 铂金价格 360.0
2023-05-05 金兰首饰 黄金价格 593.0
2023-05-05 金兰首饰 铂金价格 360.0
2023-05-05 金银街 投资金条 567.0
2023-05-05 金银街 工艺金条 582.0
2023-05-05 金银街 千足金首饰 572.0
2023-05-05 多边金都珠宝 千足金饰品 578.0
2023-05-05 多边金都珠宝 3D硬金 1121.0
2023-05-05 多边金都珠宝 精品挂件 567.0
2023-05-05 富艺珠宝 黄金价格 592.0
2023-05-05 富艺珠宝 投资金条 529.0
2023-05-05 富艺珠宝 PT950铂金 410.0
2023-05-05 天乙银饰 白银价格 5.78
2023-05-05 斯尔沃银器 白银基价 5780.0
2023-05-05 中钞国鼎 基准银价 5.817
2023-05-05 金巧福珠宝 黄金价格 607.0
2023-05-05 金巧福珠宝 铂金价格 447.0
2023-05-05 金巧福珠宝 摆件价格 407.0
2023-05-05 莱音珠宝 黄金价格 563.0
2023-05-05 莱音珠宝 铂金价格 433.0
2023-05-05 莱音珠宝 金条价格 509.0
2023-05-05 九龙福珠宝 黄金价格 593.0
2023-05-05 九龙福珠宝 铂金价格 448.0
2023-05-05 九龙福珠宝 摆件价格 412.0
[Finished in 116.6s]
'''