# -*- coding: utf-8 -*-
import scrapy
import re
import urllib
from scrapy import Request

from taobao1_spider.items import JingdongItem


class Jingdongspider(scrapy.Spider):
    name = 'jingdong'
    allowed_domains = ["jd.com"]
    start_urls = ['http://jd.com/']

    def __init__(self, keywords=None, *args, **kwargs):
        super(Jingdongspider, self).__init__(*args, **kwargs)
        print('您搜索的商品为:', keywords)
        self.keywords = keywords
        self.start_urls = ['https://search.jd.com/search?keyword=' + str(keywords) + "&enc=utf-8&wq=" + str(keywords)]

    def parse(self, response, pages=1):
        for i in range(0, int(pages)):
            url = response.url + "&page=".format(str(i*2-1))
            yield Request(url=url, callback=self.next)
        pass

    def next(self, response):
        body = response.body.decode('utf-8', 'ignore')
        shop_id = response.xpath('//ul[@class="gl-warp clearfix"]/li/@data-sku').extract()
        pad_pic = 'source-data-lazy-img="(.*?)"'
        all_pic = re.compile(pad_pic).findall(body)
        for j in range(0, len(shop_id)):
            pic = all_pic[j]
            id_url = "https://item.jd.com/" + str(shop_id[j]) + ".html"    # 进入店铺url
            yield Request(url=id_url, callback=self.next2, meta={'pic': pic})

    def next2(self, response):
        item = JingdongItem()
        item['title'] = response.xpath('//head/title/text()').extract()[0].replace('【图片 价格 品牌 报价】-京东', '')\
            .replace('【行情 报价 价格 评测】-京东', '')
        item['link'] = response.url
        # 价格抓包
        ture_id = re.findall(r'https://item.jd.com/(.*?).html', item['link'])[0]
        price_url = "https://p.3.cn/prices/mgets?skuIds=J_" + str(ture_id)  # js动态加载部分
        price_txt = urllib.request.urlopen(price_url).read().decode('utf-8', 'ignore')
        item['price'] = re.findall(r'"p":"(.*?)"', price_txt)[0]
        item['keywords'] = self.keywords
        item['pic'] = response.meta['pic']
        return item