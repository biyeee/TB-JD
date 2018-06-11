from scrapy import cmdline

cmdline.execute(['scrapy', 'crawl', 'taobao', '-a', 'keywords=苹果'])
