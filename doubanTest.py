import requests
import lxml.html

# py3.5导入etree的方式和py2.7不太一样
etree = lxml.html.etree

s = requests.Session()
for id in range(0, 251, 25):
    url = 'https://movie.douban.com/top250/?start=' + str(id)
    r = s.get(url)
    r.encoding = 'utf-8'
    root = etree.HTML(r.content)
    items = root.xpath('//ol//li/div[@class="item"]')
    for item in items:
        title = item.xpath('./div[@class="info"]//a/span[@class="title"]/text()')
        rating = item.xpath('.//div[@class="bd"]//span[@class="rating_num"]/text()')[0]
        name = title[0].encode('gb2312', 'ignore').decode('gb2312')
        with open('movie.txt', 'a') as f:
            f.write(name)
            f.write('\n')
        print(name, rating)
