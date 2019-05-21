# -*- coding: utf-8 -*-
import logging
import os
import re
import ssl
from urllib import request

from scrapy import Request

from libs.common.spider import BaseSpider, ArticleItem
from libs.config.spiders.kurir_scraper_config import (
    KURIR_NEWS_SPIDER_NAME,
    KURIR_ALLOWED_DOMAINS,
    COMMENT_SELECTOR,
    COMMENT_REGEX,
)
from libs.db.models import Article
from scrapers.news_spiders.item_loaders.kurir_item_loader import KurirArticleLoader

log = logging.getLogger(__name__)
dir_path = os.path.dirname(os.path.realpath(__file__))


class KurirNewsSpider(BaseSpider):
    name = KURIR_NEWS_SPIDER_NAME
    allowed_domains = KURIR_ALLOWED_DOMAINS

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.spider_path = dir_path

    def start_requests(self):
        for article in Article.objects(url__contains="kurir.rs/", full_article_scraped=False)[:40000]:
            yield Request(url=article.url, callback=self.parse, errback=self.error_in_response)

        failed_urls = self.get_failed_urls()
        self.clear_failed_urls_file()
        for url in failed_urls:
            yield Request(url=url, callback=self.parse, errback=self.error_in_response)

    def parse(self, response):
        try:
            loader = KurirArticleLoader(item=ArticleItem(), selector=response.selector)
            loader.add_value("url", response.url)
            item = loader.load_item()
            item["comment_count"] = self.get_comment_number(item["article_id"])
            yield item

        except Exception as e:
            log.exception(e)

    def get_comment_number(self, article_id):
        response = request.urlopen(COMMENT_SELECTOR.format(article_id), context=ssl._create_unverified_context())
        response_text = response.read()
        comment_nubmer = re.match(COMMENT_REGEX, str(response_text))

        return comment_nubmer.group(1) if comment_nubmer else 0
