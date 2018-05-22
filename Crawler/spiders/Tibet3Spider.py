import re

from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule

from Crawler.util import *
from Crawler.items import NewsItem

class TiTibet3Spider(CrawlSpider):
    name = 'tibet_tibet3'
    allowed_domains = [
        'ti.tibet3.com'
    ]

    start_urls = [
        'http://ti.tibet3.com'
    ]

    deny_urls = [
        r'.*?/video/.*?',
        r'.*?/music/.*?'
    ]
    deny_urls_ = [
        r'.*?/video/.*?',
        r'.*?/music/.*?',
    ]

    deny_domains = [
        'music.tibet3.com',
        'ti.tibet3.com/video'
    ]

    rules = (
        Rule(LinkExtractor(allow=r".*?ti.tibet3.com.*?",deny=r".*?/\d{4}-\d{2}-\d{2}/.*?"), follow=True),
        Rule(LinkExtractor(allow=r".*?/\d{4}-\d{2}-\d{2}/.*?", deny=deny_urls, deny_domains=deny_domains), callback="parse_item", follow=True)
    )

    @staticmethod
    def parse_item(response):
        sel = Selector(response)
        url = response.request.url
        if re.match(r'.*?/\d{4}-\d{2}-\d{2}/.*?html', url):

            print('---------------------')
            print(url)

            content = response.xpath('/html/body/div[1]/div[2]/div[1]/article/div[1]/p//text()').extract()
            print(content)
            # 移除编辑
            editor = response.xpath('//*[@class="-articleeditor"]/text()').extract_first()
            if editor:
                content.remove(editor)
            publish_time = sel.re(r'\d{4}-\d{2}-\d{2}.*?\d{2}:\d{2}:\d{2}')[0]
            print(publish_time)
            if ' ' in publish_time:
                publish_time = publish_time.replace(' ', '')

            if content:
                item = NewsItem(
                    domainname='http://ti.tibet3.com/',
                    chinesename='tibet3',
                    url=sel.root.base,
                    title=sel.css('.entry-header > h1:nth-child(1)::text').extract_first(),
                    subtitle=sel.css('.sub::text').extract_first(),
                    language='藏文',
                    encodingtype='utf-8',
                    corpustype='网络',
                    timeofpublish=publish_time,
                    content=''.join(content),
                    author=None
                )
                print(item.get("title", None))
                print(item.get("timeofpublish", None))
                print(item.get("source", None))
                print(item.get("author", None))
                # yield item
                item = judge_time_news(item)
                if item:
                    yield item
