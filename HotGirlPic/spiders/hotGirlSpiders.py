from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from HotGirlPic.items import HotgirlItem
import scrapy
import urllib.request
import urllib.error
import re
import os
import threading


class HotGirlPicSpider(CrawlSpider):
    name = "HotGirlPic"
    start_urls = ["http://www.mm131.com/qingchun/"]
    rules = (
        Rule(LinkExtractor(allow=('http://www.mm131.com/qingchun/\d{4,4}',),
                           deny=('http://www.mm131.com/qingchun/\d{1,6}_\d{1,2}')),
             callback='parse_item', follow=True),
    )
    lock = threading.Lock()

    def parse_item(self, response):
        item = HotgirlItem()
        maxNum = response.xpath("//div[@class='content-page']/span[@class='page-ch']/text()").re(r'共(.*?)页')[0]

        selector = Selector(response)
        item['name'] = selector.xpath('//div[@class="content"]/h5/text()').extract_first(default="N/A")
        item['url'] = response.url
        item['imgUrls'] = []

        for num in range(2, int(maxNum) + 1):
            # page_url 为每张图片所在的页面地址
            url = response.url
            page_url = url.replace('.html', '') + '_' + str(num) + '.html'

            yield scrapy.Request(page_url, meta={'item': item, 'num': str(num), 'maxNum': maxNum},
                                 callback=self.img_url)

    def img_url(self, response):
        self.lock.acquire()
        selector = Selector(response)
        imgUrl = selector.xpath('//div[@class="content-pic"]/a/img/@src').extract_first(default="N/A")
        num1 = response.meta['num']
        maxNum1 = response.meta['maxNum']
        item = response.meta['item']

        if not imgUrl in item['imgUrls']:
            item['imgUrls'].append(imgUrl)

        if len(item['imgUrls']) == int(maxNum1) - 1:
            # print('最后一个了')
            self.lock.release()
            # print(item['name'] + 'img数量' + str(len(item['imgUrls'])))
            yield item
        else:
            self.lock.release()
