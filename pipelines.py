import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
import re


class ScrapybeautiesPipeline(object):
    def process_item(self, item, spider):
        return item


class MyImagesPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None):  # 图片按照套图名称分文件夹保存
        item = request.meta['item']
        folder = item['title'][0]
        folder_strip = strip(folder)
        image_guid = request.url.split('/')[-1]
        filename = u'full/{0}/'.format(folder_strip) + str(image_guid)
        return filename

    def get_media_requests(self, item, info):
        print(item)
        for image_url in item['src']:
            print(image_url)
            yield scrapy.Request(image_url, meta={"item": item})

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        print(image_paths)
        if not image_paths:
            raise DropItem("Item contains no images")
        item['image_paths'] = image_paths
        return item


def strip(path):
    """
    :param path: 需要清洗的文件夹名字
    :return: 清洗掉Windows系统非法文件夹名字的字符串
    """
    path = re.sub(r'[？\\*|“<>:/]', '', str(path))
    return path
