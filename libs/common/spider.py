# -*- coding: utf-8 -*-
import logging
from datetime import timedelta

from scrapy import signals, Item, Field, Spider

log = logging.getLogger(__name__)


class BaseSpider(Spider):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.failed_urls = []
        self.spider_path = None

    def parse(self, response):
        pass

    def error_in_response(self, response):
        self.failed_urls.append(response.request.url)
        log.info(f"Error , code: {response.status_code}")

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(BaseSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        crawler.signals.connect(spider.add_item, signal=signals.item_passed)
        return spider

    def spider_closed(self, spider):
        log.info(f"Spider closed: {spider.name}")

    def add_item(self, item, spider):
        log.info(f"Item processed for {spider.name}: {item}")

    def get_failed_urls(self):
        urls = []
        try:
            if self.spider_path:
                with open(f"{self.spider_path}/failed_urls.txt", "r+") as urls_fle:
                    urls = urls_fle.read().splitlines()
                    self.delete_file_content(urls_fle)
        except FileNotFoundError:
            log.error("No failed_urls file!")
        finally:
            return urls

    def clear_failed_urls_file(self):
        try:
            if self.spider_path:
                with open(f"{self.spider_path}/failed_urls.txt", "r+") as urls_fle:
                    urls_fle.seek(0)
                    urls_fle.truncate()
        except FileNotFoundError:
            log.error("No failed_urls file!")

    @staticmethod
    def daterange(start_date, end_date):
        for n in range(int((end_date - start_date).days)):
            yield start_date + timedelta(n)


class ArticleItem(Item):
    url = Field()
    article_id = Field()
    title = Field()
    subtitle = Field()
    short_description = Field()
    author = Field()
    tags = Field()
    category = Field()
    subcategory = Field()
    article_datetime = Field()
    comment_count = Field()
    facebook_interaction_count = Field()
    twitter_interaction_count = Field()
    img_number = Field()
    image_urls = Field()
    number_of_instagram_links = Field()
    number_of_twitter_links = Field()
    number_of_facebook_links = Field()
    scraping_datetime = Field()


class ArchiveItem(Item):
    url = Field()
    title = Field()
    source_url = Field()
    scraping_datetime = Field()
