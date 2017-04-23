# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql.cursors
from province.items import CommitItem

class ProvincePipeline(object):
    def __init__(self):
        self.conn = pymysql.connect(host='localhost', port=3306,
                                    user='12306',
                                    password='12306',
                                    db='12306-train',
                                    charset='utf8')
        self.cursor = self.conn.cursor()
        self.sql = "INSERT IGNORE INTO `agencys` (`province`, `city`,\
                `county`, `address`, `name`, `windows`,\
                `start`, `end`) VALUES\
                (%s, %s, %s, %s, %s, %s, %s, %s)"

    def process_item(self, item, spider):
        if isinstance(item, CommitItem):
            self.conn.commit()
        else:
            self.cursor.execute(self.sql, (item["province"], item["city"],
                                           item["county"], item["address"],
                                           item["name"], item["windows"],
                                           item["start"] + u"00",
                                           item["end"] + u"00"))

