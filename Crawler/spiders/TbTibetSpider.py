import re

from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule

from Crawler.util import *
from Crawler.items import NewsItem

class TbTibetSpider(CrawlSpider):
    name = 'tb_tibet'
    allowed_domains = [
        'tb.tibet.cn'
    ]

    start_urls = [
        'http://tb.tibet.cn/'
    ]

    allow_urls = [
        r'.*?tb.tibet.cn/tb/.*?',
        r'.*?/index_.*?'
    ]
    deny_urls = [
        r'.*?/video/.*?',
        r'.*?/music/.*?'
    ]

    deny_domains = [
        'tb.tibet.cn/tb/disport',
        'tb.tibet.cn/tb/vidoe'
    ]

    rules = (
        Rule(LinkExtractor(allow=allow_urls, deny=r".*?/\d{6}/.*?", deny_domains=deny_domains), follow=True),
        Rule(LinkExtractor(allow=r".*?/\d{6}/.*?", deny=deny_urls, deny_domains=deny_domains), callback="parse_item", follow=True)
    )

    @staticmethod
    def parse_item(response):
        sel = Selector(response)
        url = response.request.url
        if re.match(r'.*?/\d{6}/.*?', url):

            # print('---------------------')
            # print(url)

            content = response.xpath('//*[@id="contentK"]/div[3]//div//text()').extract()
            # print(content)
            # 移除编辑
            editor = response.xpath('//*[@class="-articleeditor"]/text()').extract_first()
            if editor:
                content.remove(editor)
            publish_time = sel.re(r'\d{4}-\d{2}-\d{2}')[0]
            # print(publish_time)
            if ' ' in publish_time:
                publish_time = publish_time.replace(' ', '')

            if content:
                item = NewsItem(
                    domainname='http://tb.tibet.cn/',
                    chinesename='tbtibet',
                    url=sel.root.base,
                    title=sel.css('#contentK > h1::text').extract_first(),
                    subtitle=sel.css('.sub::text').extract_first(),
                    language='藏文',
                    encodingtype='utf-8',
                    corpustype='网络',
                    timeofpublish=publish_time,
                    content=''.join(content),
                    source=sel.css('#contentK > div.xinxi > span:nth-child(2)::text').extract_first(),
                    author=sel.css('#contentK > div.xinxi > span:nth-child(3)::text').extract_first()
                )
                # print(item.get("title", None))
                # print(item.get("timeofpublish", None))
                # print(item.get("source", None))
                # print(item.get("author", None))
                # yield item
                item = judge_time_news(item)
                if item:
                    yield item
