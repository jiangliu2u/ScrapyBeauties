import scrapy
from items import PicItem
from scrapy import Request

class pic_spider(scrapy.Spider):
    name = 'get_pic'
    start_urls=['https://www.meitulu.com/t/ligui/']
    img_urls = []
    
    def parse(self,response):
        all = response.xpath('/html/body/div[2]/div[3]/ul/li/a/@href').extract()
        for i in all:
            yield Request(str(i),self.get_all)
    
    def get_all(self, response):
        all = response.xpath('//*[@id="pages"]//a/@href').extract()
        for i in all:
            yield Request('https://www.meitulu.com{0}'.format(str(i)),self.get_pics)
    
    def get_pics(self, response):
        item = PicItem()
        all = response.xpath('/html/body/div[4]/center//img/@src').extract()
        for i in all:
            self.img_urls.append(i)
        item['name']=str(response.xpath('/html/head/title/text()').extract()[0]).split('_')[0].replace(' ','')
        item['image_urls']= self.img_urls
        item['url']=response.url
        yield item