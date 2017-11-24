from scrapy.spiders import CrawlSpider
from scrapy.selector import Selector
from scrapy.http import request
from HotGirlPic.items import HotgirlItem
import scrapy
import urllib.request
import urllib.error
import re
import os

class HotGirlPicSpider(CrawlSpider):
    name = "HotGirlPic"
    start_urls = ["http://www.mm131.com/qingchun/3245.html"]

    def parse(self, response):
        item = HotgirlItem()
        selector = Selector(response)
        # 当前位置
        locations = selector.xpath('//div[@class="place"]/a//text()').extract()

        item['name'] = selector.xpath('//div[@class="content"]/h5/text()').extract()
        item['imgUrl'] = selector.xpath('//div[@class="content-pic"]/a/img/@src').extract()
        imageName = selector.xpath('/span[@class=page_now]/text()').extract()
        imageUrl = '/Volumes/D/HotGirlPic/%s/%s.jpg' % (item['name'],imageName)
        if os.path.exists(imageUrl):
            print("图片存在")
        else:
            urllib.request.urlretrieve(item['imgUrl'], imageUrl)
            print("目录不存在")

