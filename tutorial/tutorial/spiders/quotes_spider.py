# -*- coding: utf-8 -*-
# @Date    : 2018-03-14 15:26:47
''' Scrapy Tutorial '''


import scrapy


class QuotesSpider(scrapy.Spider):
    name = 'quotes'

    start_urls = ['http://quotes.toscrape.com/', ]

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').extract_first(),
                'author': quote.css('small.author::text').extract_first(),
                'tags': quote.css('div.tags a.tag::text').extract(),
            }

        next_page = response.css('li.next a::attr(href)').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)


class AuthorSpider(scrapy.Spider):
    name = 'author'
    start_urls = ['http://quotes.toscrape.com/', ]

    def parse(self, response):
        for href in response.css('.author + a::attr(href)').extract():
            yield scrapy.Request(response.urljoin(href), callback=self.parse_author)

            next_page = response.css('li.next a::attr(href)').extract_first()
            if next_page is not None:
                next_page = response.urljoin(next_page)
                yield scrapy.Request(next_page, callback=self.parse)

    @staticmethod
    def parse_author(response):
        def extract_with_css(query):
            return response.css(query).extract_first().strip()

        yield {
            'name': extract_with_css('h3.author-title::text'),
            'birchdate': extract_with_css('.author-born-date::text'),
            'boi': extract_with_css('.author-description::text'),
        }
