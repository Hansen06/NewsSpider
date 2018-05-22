
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
# 运行一个
process = CrawlerProcess(get_project_settings())

process.crawl('tibet_people')
process.crawl('tibet_tibet3')
process.crawl('tb_tibet')
process.crawl('tibet_xinhua')
# process.crawl('wyxw_news')
# process.crawl('xinhua_news')
# process.crawl('sina_news')
# process.crawl('sohu_news')
# process.crawl('zhongxin_news'

process.start()
