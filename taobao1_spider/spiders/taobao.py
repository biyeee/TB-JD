# -*- coding: utf-8 -*-
import re
import urllib
import scrapy
from scrapy import Request
from taobao1_spider.items import TaobaoSpiderItem


class TaobaoSpider(scrapy.Spider):
    name = 'taobao'
    allowed_domains = ["taobao.com"]
    start_urls = ['http://taobao.com/']

    def __init__(self, keywords=None, *args, **kwargs):
        super(TaobaoSpider, self).__init__(*args, **kwargs)
        print('您搜索的商品为:', keywords)
        self.keywords = keywords
        self.start_urls = ['https://s.taobao.com/search?q=' + str(keywords)]

    def parse(self, response, pages=2):
        # key = input("请输入你要爬取的关键词\t")
        # pages = input("请输入你要爬取的页数\t")
        # key = "虾饺"
        # # pages = '100'
        # print("请输入你要搜索的关键词：",keywords)
        # self.keywords=keywords
        # print("\n")
        # print("当前爬取的关键词是", keywords)
        # print("\n")
        for i in range(0, int(pages)):
            url = response.url + "&s={}".format(str(i * 44))
            yield Request(url=url, callback=self.page)
        pass

    def page(self, response):
        body = response.body.decode('utf-8', 'ignore')
        pat_id = '"nid":"(.*?)"'  # 匹配id
        pat_now_price = '"view_price":"(.*?)"'  # 匹配价格
        pat_address = '"item_loc":"(.*?)"'  # 匹配地址
        pat_pic = '"pic_url":"(.*?)"'   # 图片

        all_id = re.compile(pat_id).findall(body)
        all_now_price = re.compile(pat_now_price).findall(body)
        all_address = re.compile(pat_address).findall(body)
        all_pic = re.compile(pat_pic).findall(body)

        for i in range(0, len(all_id)):
            this_id = all_id[i]
            now_price = all_now_price[i]
            address = all_address[i]
            pic = all_pic[i]
            url = "https://item.taobao.com/item.htm?id=" + str(this_id)
            yield Request(url=url, callback=self.next, meta={'now_price': now_price, 'address': address, 'pic': pic})
            pass
        pass

    def next(self, response):
        item = TaobaoSpiderItem()
        url = response.url
        pat_url = "https://(.*?).com"
        web = re.compile(pat_url).findall(url)

        # 淘宝和天猫的某些信息采用不同方式的Ajax加载，
        if web[0] != 'item.taobao':  # 天猫或天猫超市
            title = response.xpath("//div[@class='tb-detail-hd']/h1/text()").extract()  # 获取商品名称
            price = response.xpath("//span[@class = 'tm-price']/text()").extract()  # 获取商品原价格
            pass
        else:  # 淘宝
            title = response.xpath("//h3[@class='tb-main-title']/@data-title").extract()  # 获取商品名称
            price = response.xpath("//em[@class = 'tb-rmb-num']/text()").extract()  # 获取商品原价格
            pass

        item['keywords'] = self.keywords
        item['title'] = title
        item['link'] = url
        item['price'] = price
        item['now_price'] = response.meta['now_price']
        item['address'] = response.meta['address']
        item['pic'] = response.meta['pic']
        yield item
