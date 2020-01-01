import scrapy
from items import PicItem
from scrapy import Request
import re


class pic_spider(scrapy.Spider):
    name = 'get_pic'
    start_urls = []
    img_urls = []

    def __init__(self):
        for i in range(1, 3):
            self.start_urls.append(
                "https://www.meitulu.com/t/ligui/"+str(i)+".html")
            self.p = re.compile(r".*?_(\d+).*?html", re.S)

    def parse(self, response):
        all = response.xpath(
            '/html/body/div[2]/div[4]/ul/li/a/@href').extract()
        for i in all:
            yield Request(str(i), self.get_all)

    def get_all(self, response):
        all = response.xpath('//*[@id="pages"]//a/@href').extract()
        pages = []
        for i in all:
            aa = re.findall(self.p, i)
            if len(aa) == 0:
                pages.append(i)
        last = re.findall(self.p, all[-2])
        num = int(last[0]) + 1
        for page in range(2,num):
            u = pages[0].replace(".html","_{}.html".format(page))
            pages.append(u)
        for i in pages:
            yield Request('https://www.meitulu.com{0}'.format(str(i)), self.get_pics)

    def get_pics(self, response):
        item = PicItem()
        all = response.xpath('/html/body/div[4]/center//img/@src').extract()
        for i in all:
            self.img_urls.append(i)
        item['name'] = str(response.xpath(
            '/html/head/title/text()').extract()[0]).split('_')[0].replace(' ', '')
        item['image_urls'] = self.img_urls
        item['url'] = response.url
        yield item
