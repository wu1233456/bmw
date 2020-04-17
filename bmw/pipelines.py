# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pathlib import Path
from urllib import request
from scrapy.pipelines.images import ImagesPipeline
from bmw import settings
import os
from scrapy.http import Request


class BmwPipeline(object):
    # 由于使用了自定义的类，该类不会被执行
    def __init__(self):
        p = Path()
        url = p.resolve()
        self.url = Path(url, 'imges')
        url.mkdir(exist_ok=True)

    def process_item(self, item, spider):
        title = item['title']
        hrefs = item['hrefs']
        path = Path(self.url, title)
        path.mkdir(exist_ok=True)
        for href in hrefs:
            imagesame = href.split('_')[-1]
            request.urlretrieve(href, Path(path, imagesame))

        return item


class BmwImagesPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None):
        # 该方法是在图片将要被存储的时候调用，来获取这个图片存储路径
        path = super(BmwImagesPipeline, self).file_path(request, response, info)
        title = request.item.get('title')
        images_store = settings.IMAGES_STORE
        category_path = Path(images_store, title)
        category_path.mkdir(exist_ok=True)
        image_name = path.replace('full/', '')
        image_path = Path(category_path, image_name)
        print(image_path)
        image_path = os.path.join(title, image_name)
        return image_path
    # 重写父类的下面两个方法
    def get_media_requests(self, item, info):
        # 这个方法是在发送下载请求之前调用的，其实这个方法本身就是去发送下载请求的
        request_objs = super(BmwImagesPipeline, self).get_media_requests(item, info)
        for request_obj in request_objs:
            request_obj.item = item
        return request_objs

