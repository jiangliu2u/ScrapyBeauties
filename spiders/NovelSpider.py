import scrapy
from bs4 import BeautifulSoup
from scrapy.http import Request
from dingdian.items import DingdianItem
class MySpider(scrapy.Spider):
	
    name = 'novelSpider'
    allowed_domains = ['x23us.com']
    bash_url = 'http://www.x23us.com/class/'
    bashurl = '.html'
    f = open('D:/Novel_Info.txt','w+')
    def start_requests(self):
        
        for i in range(1, 11):
            url = self.bash_url + str(i) + '_1' + self.bashurl
            yield Request(url, self.parse)
        yield Request('http://www.x23us.com/quanben/1', self.parse)
 
    def parse(self, response):
		max_num = BeautifulSoup(response.text,'lxml').find('div',class_='pagelink').find_all('a')[-1].get_text()
		bashurl = str(response.url)[:-7]
		for num in range(1, int(max_num)+1):
                    url = bashurl + '_' + str(num) +self.bashurl
                    yield Request(url,callback = self.get_name)
	
    def get_name(self, response):
		tds = BeautifulSoup(response.text,'lxml').find_all('tr',bgcolor = '#FFFFFF')
		for td in tds:
			novelname = td.find('a',attrs={'target':'_blank'}).get_text()
			novelurl = td.find('a')['href']
			self.f.write(novelname.encode('utf-8')+': '+novelurl+'\n')
			print novelname,': ',novelurl
	
	
