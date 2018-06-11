# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql


class Taobao1SpiderPipeline(object):

    def __init__(self, settings):
        self.settings = settings

    def process_item(self, item, spider):
        print(item)
        if spider.name == "taobao":
            self.cursor.execute("""insert into taobao(pName,pTitle,pUrl,bPrice,nPrice,address,cId,sId,pic_url,source)
                          values ("%s","%s","%s","%s","%s","%s",'1','1',"%s",'淘宝')""",
                                (item['keywords'], item['title'], item['link'], item['price'], item['now_price'],
                                    item['address'], item['pic']))
        elif spider.name == "jingdong":
            self.cursor.execute("""insert into jingdong(pName,pTitle,pUrl,bPrice,pic_url,source)values
                                           ("%s","%s","%s","%s","%s","京东")""",
                                (item['keywords'], item['title'], item['link'], item['price'], item['pic']))
        else:
            spider.log('Undefined name:%s' % spider.name)
        return item

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def open_spider(self,spider):
        # 连接数据库
        self.connect = pymysql.connect(
            host=self.settings.get('MYSQL_HOST'),
            port=self.settings.get('MYSQL_PORT'),
            db=self.settings.get('MYSQL_DBNAME'),
            user=self.settings.get('MYSQL_USER'),
            passwd=self.settings.get('MYSQL_PASSWD'),
            charset='utf8',
            use_unicode=True
        )
        # 通过cursor执行增删查改
        self.cursor = self.connect.cursor();
        self.connect.autocommit(True)

    def close_spider(self, spider):
        self.cursor.close()
        self.connect.close()
