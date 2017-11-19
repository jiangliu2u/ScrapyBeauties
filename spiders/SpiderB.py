import scrapy
from bs4 import BeautifulSoup
from scrapy.http import Request
import re
from lxml import etree
import os
import urllib.request
import urllib
from items import ScrapybeautiesItem


class MySpider2(scrapy.Spider):
    name = 'NewSpider'
    start_url = 'http://www.umei.cc/p/gaoqing/cn/'
    f = open('D:/T.txt', 'w+')

    def start_requests(self):
        #for i in range(2):
        url = self.start_url + str(1) + '.htm'
        yield Request(url, self.parse)  # 获取每页中套图地址，共22页

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'lxml').find('div', class_='TypeList').find_all('a',
                                                                                            attrs={
                                                                                                "class": "TypeBigPics"})
        urls = [x.get('href') for x in soup]  # 获取每个页面中套图的地址
        for i in urls:
            yield Request(i, self.getPicUrls)

    def getPicUrls(self, response):  # 获取套图中每张照片所在页面的地址
        soup = BeautifulSoup(response.text, 'lxml').find('div', class_='NewPages').find('a').text
        nums = re.findall("\d+", soup)[0]  # 获取套图总页数
        soup2 = BeautifulSoup(response.text, 'lxml').find('div', class_='NewPages').find_all('a')
        pageUrl = soup2[-1]['href']
        p2 = pageUrl.split('/')[-1]
        p3 = p2.split('_')[0]  # 获取套图的id
        page = 'http://www.umei.cc/p/gaoqing/cn/' + p3
        title = BeautifulSoup(response.text, 'lxml').find('title').text
        for i in range(1, int(nums)):
            pic_url = page + '_' + str(i) + '.htm'
            yield Request(pic_url, self.getPics)


    def getPics(self, response):  # 获取每张图片的地址
        item = ScrapybeautiesItem()
        sr = response.xpath('//*[@id="ArticleId0"]/p/img/@src').extract()
        item['src'] = sr[0]
        #item['alt'] = '1'
        #item['title'] = '2'
        yield item

        # def mkdir(self, path):  # 这个函数创建文件夹
        #     isExists = os.path.exists(os.path.join("D:\mzitu", path))
        #     if not isExists:
        #         print(u'建了一个名字叫做', path, u'的文件夹！')
        #         os.makedirs(os.path.join("D:\mzitu", path))
        #         os.chdir(os.path.join("D:\mzitu", path))  ##切换到目录
        #         return True
        #     else:
        #         print(u'名字叫做', path, u'的文件夹已经存在了！')
        #         return False
        #
        # def save(self, img_url):  # 保存图片
        #     name = img_url.replace('http://i1.umei.cc/uploads/tu/', '')
        #     name2 = name.replace('/', '_')
        #     print(img_url)
        #     img = urllib.request.urlopen(img_url)
        #     data = img.read()
        #     print('hahha')
        #     f = open(name2 + '.jpg', 'ab')
        #     f.write(data)
        #     print('xxxx')
        #     f.close()
