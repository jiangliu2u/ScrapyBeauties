# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapybeautiesItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()  # 套图标题
    src = scrapy.Field()  # 图片链接
    images = scrapy.Field()
    image_paths = scrapy.Field()
