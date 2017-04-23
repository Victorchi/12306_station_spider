# -*- coding: utf-8 -*-
import scrapy


class NameSpider(scrapy.Spider):
    name = "name"
    allowed_domains = ["province"]
    start_urls = ['http://province/']

    def parse(self, response):
        pass
