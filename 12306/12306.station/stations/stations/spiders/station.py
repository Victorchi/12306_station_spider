# -*- coding: utf-8 -*-
import scrapy
import urllib
from scrapy.http.request import Request
from stations.items import StationItem
from stations.items import CommitItem
import json

class StationSpider(scrapy.Spider):
    name = "station"
    start_urls = ['http://www.12306.cn/mormhweb/kyyyz/']

    custom_settings = {
        'ITEM_PIPELINES': {
            'stations.pipelines.StationsPipeline': 300,
        },
    }

    def parse(self, response):
        names = response.css("#secTable > tbody > tr > td::text").extract()
        sub_urls = response.css("#mainTable td.submenu_bg > a::attr(href)").extract()
        for i in range(0, len(names)):
            sub_url1 = response.url + sub_urls[i * 2][2:]
            yield Request(sub_url1, callback=self.parse_station, meta={'bureau': names[i], 'station': True})

            sub_url2 = response.url + sub_urls[i * 2 + 1][2:]
            yield Request(sub_url2, callback=self.parse_station, meta={'bureau': names[i], 'station': False})

    def parse_station(self, response):
        datas = response.css("table table tr")
        if len(datas) <= 2:
            return
        for i in range(0, len(datas)):
            if i < 2:
                continue
            infos = datas[i].css("td::text").extract()

            item = StationItem()
            item["bureau"] = response.meta["bureau"]
            item["station"] = response.meta["station"]
            item["name"] = infos[0]
            item["address"] = infos[1]
            item["passenger"] = infos[2].strip() != u""
            item["luggage"] = infos[3].strip() != u""
            item["package"] = infos[4].strip() != u""
            yield item
        yield CommitItem()

