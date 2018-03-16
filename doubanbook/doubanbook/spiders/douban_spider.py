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
        Rule(LinkExtractor(allow=('/subject/\d+/$')), callback='parse_2'),
        Rule(LinkExtractor(allow=('/tag/[^/]+$', )), follow=True),
    ]
    logger = logging.getLogger('doubanbook')

    def parse_1(self, response):
        self.logger.info('parsed ' + str(response))

    def parse_2(self, response):
        self.logger.info('link: ' + response.url)
        items = []
        sel = Selector(response)
        sites = sel.css('#wrapper')

        for site in sites:
            item = DoubanSubjectItem()
            item['title'] = ''.join(site.css('h1 span::text').extract())
            item['url'] = response.url
            item['rate'] = float(site.css('.ll.rating_num::text').extract_first().strip())
            item['votes'] = int(site.css('span [property="v:votes"]::text').extract_first())
            intro = site.css('.related_info .indent .intro')
            content_intro = site.css('#link-report .intro')
            item['content_intro'] = ''.join(content_intro[-1].css('p::text').extract())
            if len(intro) > len(content_intro):
                item['author_intro'] = ''.join(intro[-1].css('p::text').extract())
            else:
                item['author_intro'] = ''
            item['tags'] = ', '.join(site.css('#db-tags-section a::text').extract())
            items.append(item)
        return items

    def process_request(self, request):
        self.logger.info('process ' + str(request))
        return request

    def closed(self, reason):
        self.logger.info('DoubanbookSpider Closed: ' + reason)
