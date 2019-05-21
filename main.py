import os
import sys

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from libs.config.crawler_config import CRAWLER_CONFIG


def crawl():
    spider_name = sys.argv[1]
    settings = CRAWLER_CONFIG[spider_name]

    if os.environ.setdefault("SCRAPY_SETTINGS_MODULE", settings) != settings:
        os.environ.pop("SCRAPY_SETTINGS_MODULE")
        os.environ.setdefault("SCRAPY_SETTINGS_MODULE", settings)

    crawler = CrawlerProcess(get_project_settings())
    spider = crawler.spider_loader.load(spider_name)
    crawler.crawl(spider)
    crawler.start()
    crawler.stop()


crawl()
