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
    # headers = {
    #     'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    #     'Accept-Encoding':'gzip,deflate',
    #     'Accept-Language':'zh-CN,zh;q=0.9',
    #     'Connection' : 'keep-alive',
    #     'Host' : 'img1.mm131.me',
    #     'Cache-Control': 'max-age=0',
    #     'Referer':'http://www.mm131.com/qingchun/3245.html'
    # }

    def parse(self, response):
        item = HotgirlItem()
        selector = Selector(response)
        # 当前位置
        locations = selector.xpath('//div[@class="place"]/a//text()').extract()

        item['name'] = selector.xpath('//div[@class="content"]/h5/text()').extract()
        item['imgUrl'] = selector.xpath('//div[@class="content-pic"]/a/img/@src').extract()
        imageName = selector.xpath('//span[@class="page_now"]/text()').extract()[0]

        #mac
        # imagePath = '/Volumes/D/HotGirlPic/%s/%s.jpg' % (item['name'],imageName)
        # foldUrl = '/Volumes/D/HotGirlPic/%s' % (item['name'])

        #windows
        imagePath = 'J:\HotGirlPic\%s\%s.jpg' % (item['name'][0], imageName)
        foldUrl = 'J:\HotGirlPic\%s' % (item['name'][0])

        if os.path.exists(foldUrl):
            pass
        else:
            os.makedirs(foldUrl)

        if os.path.exists(imagePath):
            print("图片存在")
        else:
            opener = urllib.request.build_opener()
            headers = (
            'If-Modified-Since','Fri, 24 Nov 2017 11:49:33 GMT')
            opener.addheaders = [headers]
            urllib.request.install_opener(opener)
            urllib.request.urlretrieve(item['imgUrl'][0], imagePath)

