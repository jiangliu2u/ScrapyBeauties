import scrapy
from items import PicItem
from scrapy import Request

class pic_spider(scrapy.Spider):
    name = 'get_pic'
    start_urls=['http://www.ivsky.com/bizhi/fengjing/']
    img_urls = []
    
    def parse(self,response):
        all = response.xpath('/html/body/div[3]/div[6]/ul//li/div/a/@href').extract()
        for i in all:
            yield Request('http://www.ivsky.com{0}'.format(str(i)),self.get_all)
    
    def get_all(self, response):
        all = response.xpath('/html/body/div[3]/div[4]/ul//li/div/a/@href').extract()
        for i in all:
            yield Request('http://www.ivsky.com{0}'.format(str(i)),self.get_pics)
    
    def get_pics(self, response):
        item = PicItem()
        all = response.xpath('//*[@id="imgis"]/@src').extract()[0]
        self.img_urls.append(all)
        item['name']=str(response.xpath('//*[@id="al_tit"]/h1/text()').extract()[0]).split(' ')[0]
        item['image_urls']= self.img_urls
        yield item