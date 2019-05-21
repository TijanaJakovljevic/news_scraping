# -*- coding: utf-8 -*-
import logging
from datetime import datetime

from scrapy import Request

from libs.common.spider import BaseSpider, ArticleItem
from libs.config.spiders.novosti_scraper_config import NOVOSTI_SPIDER_NAME, NOVOSTI_ALLOWED_DOMAINS
from libs.db.models import Article
from scrapers.news_spiders.item_loaders.novosti_item_loader import NovostiLoader

log = logging.getLogger(__name__)


class NovostiSpider(BaseSpider):
    name = NOVOSTI_SPIDER_NAME
    allowed_domains = NOVOSTI_ALLOWED_DOMAINS

    def start_requests(self):
        for article in Article.objects(url__contains="novosti.rs", full_article_scraped=False):
            yield Request(url=article.url, callback=self.parse, errback=self.error_in_response)

    def parse(self, response):
        try:
            loader = NovostiLoader(item=ArticleItem(), selector=response.selector)
            loader.add_value("url", response.url)
            loader.add_value("scraping_datetime", datetime.now())
            yield loader.load_item()

        except Exception as e:
            log.exception(e)
