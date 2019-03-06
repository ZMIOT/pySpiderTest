import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import lxml
import os
import random
import json
from urllib import parse
import re


Hostreferer = {
    'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)',
    'Referer': 'http://www.mzitu.com'
}
Picreferer = {
    'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)',
    'Referer': 'http://i.meizitu.net'
}



#抓取一个图集的图片
def get_one_images(url,name):
    r=requests.get(url,headers=Picreferer)
    html=r.text
    soup=BeautifulSoup(html,'lxml')
    pages=soup.select('#entry-content > div.post-links > a')
    pagenumber=len(pages)+1
    i=0
    root='D:\meizitu/'
    roots=root+name+'/'
    for x in range(pagenumber):
        urls=url+'/'+str(x+1)
        #print(urls)
        soup1=BeautifulSoup(requests.get(urls).text,'lxml')
        imgs=soup1.select('img[class="po-img-big"]')
        for image in imgs:
            path = roots + str(i) + '.jpg'
            if not os.path.exists(roots):
                os.mkdir(roots)
            name=image.get('alt')
            img=image.get('src')
            req=requests.get(img)
            with open(path,'wb') as f:
                f.write(req.content)
            i=i+1
#获取多个图集的url
def get_imglist(urls):
    #loadMore(action)
    souplist1 = BeautifulSoup(requests.get(urls,headers=Hostreferer).text, 'lxml')
    alist = souplist1.select('#comments > div.box > ol > li')
    imgs=souplist1.find_all('img',src=re.compile(r'^http://.+[.jpg or .gif]'))
    urllist=[]
    for a in imgs:
        urllist.append(a.get('src'))
    print(urllist)
    for url in urllist:
        get_one_images(url,generate_random_str())

#随机生成一个字符串作为图集名称
def generate_random_str(randomlength=16):
    """
    生成一个指定长度的随机字符串
    """
    random_str = ''
    base_str = 'ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789'
    length = len(base_str) - 1
    for i in range(randomlength):
        random_str += base_str[random.randint(0, length)]
    return random_str


def loadMore(action):
    rest=[]
    text=json.dumps(action)
    url="https://www.ifzsa.com/wp-admin/admin-ajax.php?action="+parse.quote(text)
    res=requests.get(url,headers=Hostreferer)




if __name__=='__main__':
    # url='https://www.ifzsa.com/2018/51793.html'
    # get_one_images(url)
    urls = 'https://www.ifzsa.com/2015/32353.html'
    get_imglist(urls)
