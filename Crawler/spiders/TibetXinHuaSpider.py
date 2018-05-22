import re

from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule

from Crawler.util import *
from Crawler.items import NewsItem

class TibetXinHuaSpider(CrawlSpider):
    name = 'tibet_xinhua'
    allowed_domains = [
        'xizang.news.cn'
    ]

    start_urls = [
        'http://xizang.news.cn/'
    ]

    deny_urls = [

    ]

    deny_domains = [

    ]

    rules = (
        Rule(LinkExtractor(allow=r".*?xizang.news.cn/.*?/index.*?", deny=r".*?xizang.news.cn/.*?/\d{4}-\d{2}/\d{2}/.*?" ), follow=True),
        Rule(LinkExtractor(allow=r".*?xizang.news.cn/.*?/\d{4}-\d{2}/\d{2}/.*?", deny=r".*?xizang.news.cn/.*?/index.*?" ), callback="parse_item", follow=True)
    )

    @staticmethod
    def parse_item(response):
        sel = Selector(response)
        url = response.request.url
        if re.match(r'.*?/\d{4}-\d{2}/\d{2}/.*?', url):

            print('---------------------')
            print(url)
            content = response.xpath('/html/body/div[6]/div/div/div[3]//p//text()').extract()
            print(content)
            # 移除编辑
            editor = response.xpath('//*[@class="-articleeditor"]/text()').extract_first()
            if editor:
                content.remove(editor)
            publish_time = sel.re(r'\d{4}-\d{2}-\d{2}')[0]
            print(publish_time)
            if ' ' in publish_time:
                publish_time = publish_time.replace(' ', '')

            if content:
                item = NewsItem(
                    domainname='http://xizang.news.cn/',
                    chinesename='tibetxinhua',
                    url=sel.root.base,
                    title=sel.css('#ArticleTit::text').extract_first(),
                    subtitle=sel.css('.sub::text').extract_first(),
                    language='藏文',
                    encodingtype='utf-8',
                    corpustype='网络',
                    timeofpublish=publish_time,
                    content=''.join(content),
                    source=sel.css('#Articlely > div.laiyuan > a::text').extract_first(),
                    author=sel.css('#contentK > div.xinxi > span:nth-child(3)::text').extract_first()
                )
                print(item.get("title", None))
                print(item.get("timeofpublish", None))
                print(item.get("source", None))
                print(item.get("author", None))
                # yield item
                item = judge_time_news(item)
                if item:
                    yield item
