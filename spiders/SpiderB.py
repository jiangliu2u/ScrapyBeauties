import scrapy
from bs4 import BeautifulSoup
from scrapy.http import Request
import re
from items import ScrapybeautiesItem


class MySpider2(scrapy.Spider):
    name = 'NewSpider'
    start_url = ['http://www.umei.cc/p/gaoqing/cn/']
    f = open('D:/T.txt', 'w+')

    def start_requests(self):
        for i in range(23):
            url = self.start_url[0] + str(i) + '.htm'
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
        title = response.xpath("/html/head/title").extract()
        item['src'] = [sr[0]]  # !!!!!!注意此处url要保存为list中，方便imagepielines下载
        item['title'] = [title[0].split('[')[1].replace("]", '').replace(' ', '')]  # 标题去除空格，防止存盘时写入出错
        yield item
