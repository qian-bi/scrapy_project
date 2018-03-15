# -*- coding: utf-8 -*-
# @Date    : 2018-03-15 09:42:51

import logging
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from doubanbook.items import DoubanSubjectItem


class DoubanbookSpider(CrawlSpider):
    name = 'doubanbook'
    allowed_domains = ['douban.com']
    start_urls = ['https://book.douban.com/tag/']
    rules = [
        Rule(LinkExtractor(allow=('/subject/\d+$', )), callback='parse_2'),
        Rule(LinkExtractor(allow=('/tag/[^/]+$', )), follow=True),
    ]
    logger = logging.getLogger('doubanbook')

    def parse_1(self, response):
        self.logger.info('parsed ' + str(response))

    @staticmethod
    def parse_2(response):
        items = []
        sel = Selector(response)
        sites = sel.css('#wraper')

        for site in sites:
            item = DoubanSubjectItem()
            item['title'] = site.css('h1 span::text').extract()
            site['url'] = response.url
            item['content_intro'] = site.css('#link-report .intro p::text').extract()
            items.append(item)
        return items

    def process_request(self, request):
        self.logger.info('process ' + str(request))
        return request

    def closed(self, reason):
        self.logger.info('DoubanbookSpider Closed: ' + reason)
