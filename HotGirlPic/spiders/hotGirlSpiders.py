from scrapy.spiders import CrawlSpider,Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from HotGirlPic.items import HotgirlItem
import scrapy
import urllib.request
import urllib.error
import re
import os

class HotGirlPicSpider(CrawlSpider):
    name = "HotGirlPic"
    start_urls = ["http://www.mm131.com/qingchun/"]
    img_urls = []
    rules = (
        Rule(LinkExtractor(allow=('http://www.mm131.com/qingchun/\d{4,4}',), deny=('http://www.mm131.com/qingchun/\d{1,6}_\d{1,2}')),
             callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = HotgirlItem()
        maxNum = response.xpath("//div[@class='content-page']/span[@class='page-ch']/text()").re(r'共(.*?)页')[0]

        selector = Selector(response)
        item['name'] = selector.xpath('//div[@class="content"]/h5/text()').extract_first(default="N/A")
        item['url'] = response.url

        for num in range(2, int(maxNum)):
            # page_url 为每张图片所在的页面地址
            url = response.url
            page_url = url.replace('.html', '') + '_' + str(num) + '.html'
            yield scrapy.Request(page_url, callback=self.img_url)

        item['imgUrls'] = self.img_urls
        yield item

    def img_url(self, response, ):
        selector = Selector(response)
        imgUrl = selector.xpath('//div[@class="content-pic"]/a/img/@src').extract_first(default="N/A")

        self.img_urls.append(imgUrl)

    # def parse(self, response):
    #     item = HotgirlItem()
    #     selector = Selector(response)
    #     # 当前位置
    #     locations = selector.xpath('//div[@class="place"]/a//text()').extract()
    #
    #     item['name'] = selector.xpath('//div[@class="content"]/h5/text()').extract()
    #     item['imgUrl'] = selector.xpath('//div[@class="content-pic"]/a/img/@src').extract()
    #     imageName = selector.xpath('//span[@class="page_now"]/text()').extract()[0]
    #
    #     #mac
    #     imagePath = '/Volumes/D/HotGirlPic/%s/%s.jpg' % (item['name'][0],imageName)
    #     foldUrl = '/Volumes/D/HotGirlPic/%s' % (item['name'][0])
    #
    #     #windows
    #     # imagePath = 'J:\HotGirlPic\%s\%s.jpg' % (item['name'][0], imageName)
    #     # foldUrl = 'J:\HotGirlPic\%s' % (item['name'][0])
    #
    #     if os.path.exists(foldUrl):
    #         pass
    #     else:
    #         os.makedirs(foldUrl)
    #
    #     if os.path.exists(imagePath):
    #         print("图片存在")
    #     else:
    #         # opener = urllib.request.build_opener()
    #         # headers = (
    #         # 'If-Modified-Since','Fri, 24 Nov 2017 11:49:33 GMT')
    #         # opener.addheaders = [headers]
    #         # urllib.request.install_opener(opener)
    #         urllib.request.urlretrieve(item['imgUrl'][0], imagePath)

