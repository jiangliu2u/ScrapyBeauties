import urllib.request

import scrapy
from bs4 import BeautifulSoup
from scrapy.http import Request
import re


class BeautySpider(scrapy.Spider):
    name = 'BeautyPic'
    siteURL = "http://www.umei.cc/p/gaoqing/cn/"

    def start_requests(self):
        for i in range(1, 23):
            url = self.siteURL + str(i) + '.htm'
            yield Request(url, self.parse)  # 获取每页中套图地址，共22页

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'lxml').find('div', class_='TypeList').find_all('a',
                                                                                            attrs={
                                                                                                "class": "TypeBigPics"})
        urls = [x.get('href') for x in soup]
        for i in urls:
            request2 = urllib.request.Request(i)
            resp = urllib.request.urlopen(request2)
            nums = self.getPageNums(resp)
            yield self.getPicUrls(i, nums)


            # print(urls)

    def getPicUrls(self, url, pageNums):

        url_fix = url.replace('.htm', '')
        u = []

        for i in range(1, int(pageNums) + 1):
            img_u = url_fix + '_' + str(i) + '.htm'
            # print(img_u)
            request3 = urllib.request.Request(img_u)
            page_content = urllib.request.urlopen(request3)
            img_info = BeautifulSoup(page_content, 'lxml').find('div', class_='ImageBody').find('img')
            img_url = img_info.get('src')  # 获当前图片地址
            u.append(img_url)
        print(u)

    def getPageNums(self, response):
        soup2 = BeautifulSoup(response, 'lxml').find('div', class_='NewPages').find('a')
        nums = re.findall("\d+", soup2.text)[0]  # 获取套图总页码数
        return nums
