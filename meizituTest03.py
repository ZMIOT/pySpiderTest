import requests
from bs4 import BeautifulSoup
import os
from PIL import Image

import lxml.html

etree=lxml.html.etree

Hostreferer = {
    'User-Agent':'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)',
    'Referer':'http://www.mzitu.com'
}
Picreferer = {
    'User-Agent':'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)',
    'Referer':'http://i.meizitu.net'
}

def get_page_name(url):#获得图集最大页数和名称
    s = requests.Session()
    r = s.get(url)
    r.encoding = 'utf-8'
    root = etree.HTML(r.content)

    name=root.xpath('//*[@id="post-single"]/h1/text()')
    return name

def get_html(url):#获得页面html代码
    req = requests.get(url, headers=Hostreferer)
    html = req.text
    return html

def get_img_url(url, name):
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')
    img_url = soup.find('img', alt= name)
    return img_url['src']

def save_img(img_url, count, name):
    req = requests.get(img_url, headers=Picreferer)
    print("this is a content")
    print(req.content)
    with open(name+'/'+str(count)+'.jpg', 'wb') as f:
        f.write(req.content)

def main():
    old_url = "https://www.ifzsa.com/blog/2018/12/01/%E6%B0%94%E8%B4%A8%E9%95%BF%E8%85%BF%E9%85%A5%E8%83%B8%E7%BE%8E%E5%A5%B3%E6%80%A7%E6%84%9F%E5%9B%BE%E7%89%87/"
    page, name = get_page_name(old_url)
    os.mkdir(name)
    for i in range(1, len(page)+1):
        url = old_url + "/" + str(i)
        img_url = get_img_url(url, name)
        #print(img_url)
        save_img(img_url, i, name)
        print('保存第' + str(i) + '张图片成功')
main()