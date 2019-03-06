# -*- coding: utf-8 -*-
import requests
import os
from bs4 import BeautifulSoup
import json
import urllib.request
from urllib import error
from tqdm import tqdm





Picreferer = {
    'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)',
    'Referer': 'http://i.meizitu.net'
}

Headers={
    'Host':'91qz.vip',
    'Referer':'http://91qz.vip/xvh5play',
    'Content-Type':'application/x-www-form-urlencoded',
    'Accept':'application/json, text/plain, */*',
    'Accept-encoding':'gzip, deflate',
    'Origin':'http://91qz.vip',
    'Content-Length': '28',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36',
}

def download_file(url):
    urls = 'http://91qz.vip/ttsp/xvinfo/?u=L3ZpZGVvNDQ0MjUyNDMvY29uX2dhaV95ZXVfY3VhX2JvLl9mdWxsX2hkX2F0X2h0dHBzX2xpbms0d2luLmxpdmVfZnlrYWJnMW4='
    r=requests.get(urls,stream=True)
    soup=BeautifulSoup(r.text,'lxml')
    jsonstr=json.loads(soup.text,'utf-8')
    videoUrl=jsonstr.get('mp4')
    print(videoUrl)
    r=requests.get(videoUrl,stream=True)
    chunk_size=1024
    print('下载开始')
    root = 'D:\Video/'
    path=root+str("av")+'.avi'
    if not os.path.exists(root):
        os.mkdir(root)
    with open(path, "wb") as f:
        for chunk in tqdm(r.iter_content(chunk_size=chunk_size)):
            f.write(chunk)
    print("下载完成")

if __name__ == '__main__':
    url = 'http://91qz.vip/xvh5play'
    soup=BeautifulSoup(requests.get(url,headers=Headers).text,"lxml")
    download_file(url)