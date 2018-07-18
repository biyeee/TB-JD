# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
import pymongo

class MongoPipeline(object):
    collection_name1 = 'taobao'
    collection_name2 = 'jingdong'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if spider.name == "taobao":
            self.db[self.collection_name1].update({'title': item['title']}, dict(item), True)  # 去重
        elif spider.name == "jingdong":
            self.db[self.collection_name2].update({'title': item['title']}, dict(item), True)  # 去重
        return item


# class Taobao1SpiderPipeline(object):
#
#     def __init__(self, settings):
#         self.settings = settings
#
#     def process_item(self, item, spider):
#         print(item)
#         if spider.name == "taobao":
#             self.cursor.execute("""insert into taobao(pTitle,pName,pUrl,bPrice,nPrice,address,cId,sId,pic_url)
#                           values ("%s","%s","%s","%s","%s","%s",'1','1',"%s")""",
#                                 (item['title'], item['keywords'], item['link'], item['price'], item['now_price'],
#                                     item['address'], item['pic']))
#         elif spider.name == "jingdong":
#             self.cursor.execute("""insert into jingdong(pName,pTitle,pUrl,bPrice,pic_url,source)values
#                                            ("%s","%s","%s","%s","%s","京东")""",
#                                 (item['keywords'], item['title'], item['link'], item['price'], item['pic']))
#         else:
#             spider.log('Undefined name:%s' % spider.name)
#         return item
#
#     @classmethod
#     def from_crawler(cls, crawler):
#         return cls(crawler.settings)
#
#     def open_spider(self,spider):
#         # 连接数据库
#         self.connect = pymysql.connect(
#             host=self.settings.get('MYSQL_HOST'),
#             port=self.settings.get('MYSQL_PORT'),
#             db=self.settings.get('MYSQL_DBNAME'),
#             user=self.settings.get('MYSQL_USER'),
#             passwd=self.settings.get('MYSQL_PASSWD'),
#             charset='utf8',
#             use_unicode=True
#         )
#         # 通过cursor执行增删查改
#         self.cursor = self.connect.cursor();
#         self.connect.autocommit(True)
#
#     def close_spider(self, spider):
#         self.cursor.close()
#         self.connect.close()
