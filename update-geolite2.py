#!/usr/bin/env python3
# coding: utf-8
import requests
import time
import tarfile
import glob
import shutil
import os
from random import choice
#import urllib3
#urllib3.disable_warnings()
import logging
logging.captureWarnings(True)

def downloadFile(url, localfile):
    try:
        headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36' }
        r = requests.get(url, headers = headers, verify =False, timeout=(3,7))
        with open(localfile, "wb") as f:
            time.sleep(choice(range(500,3500))/1000)
            f.write(r.content)
    except Exception as err:
        print(err)

def untar(fname, dirs):
    t = tarfile.open(fname)
    t.extractall(path = dirs)

def get_geolite():
    license_key = 'xxx'
    for edition_id in ('ASN','City','Country'):
        url = f'https://download.maxmind.com/app/geoip_download?edition_id=GeoLite2-{edition_id}&license_key={license_key}&suffix=tar.gz'
        filename = f'GeoLite2-{edition_id}.tar.gz'
        downloadFile(url, filename)
        untar(filename, './')
 
    print(list(glob.iglob('./GeoLite2*/*.mmdb')))
    for mmdbfile in glob.iglob('./GeoLite2*/*.mmdb'): shutil.copy(mmdbfile,'./')
    for filename in glob.iglob('GeoLite2-*_*'): shutil.rmtree(filename)
    for filename in glob.iglob('GeoLite2*.gz'): os.remove(filename)

if __name__ == '__main__':
    t1 = time.time()
    get_geolite()
    t2 = time.time()
    print('It takes %d seconds.' % (int(t2-t1)))

