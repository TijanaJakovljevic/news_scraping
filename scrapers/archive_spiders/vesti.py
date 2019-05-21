# -*- coding: utf-8 -*-
import logging
from datetime import datetime

import scrapy
from scrapy import Request

from libs.common.spider import BaseSpider, ArchiveItem
from libs.config.spiders.vesti_scraper_config import (
    VESTI_SPIDER_NAME,
    VESTI_ALLOWED_DOMAINS,
    BASE_URL_TEMPLATE,
    SOURCES,
    INNER_LINK_SELECTOR,
    REDIRECT_LINK_SELECTOR,
    NUMBER_OF_PAGES_SELECTOR,
    START_DATE,
    END_DATE,
)
from libs.db.client import connect_to_database
from libs.db.models import Article

log = logging.getLogger(__name__)


class VestiSpider(BaseSpider):
    name = VESTI_SPIDER_NAME
    allowed_domains = VESTI_ALLOWED_DOMAINS

    def __init__(self, *args, **kwargs):
        super(VestiSpider, self).__init__(*args, **kwargs)

        connect_to_database()
        self.existing_news_list = list(Article.objects.values_list("source_url"))

    def start_requests(self):
        for source in SOURCES:
            for date in BaseSpider.daterange(START_DATE, END_DATE):
                url = BASE_URL_TEMPLATE.format(year=date.year, month=date.month, day=date.day, source=source)
                yield Request(
                    url=url, callback=self.get_number_of_pages_for_date_and_source, errback=self.error_in_response
                )

    def get_number_of_pages_for_date_and_source(self, response):
        number_of_pages = response.selector.xpath(NUMBER_OF_PAGES_SELECTOR).extract()[-1]

        for page in range(1, int(number_of_pages)):
            url = response.url + str(page) + "/"
            yield Request(url=url, callback=self.get_archive_news_for_date_and_source, errback=self.error_in_response)

    def get_archive_news_for_date_and_source(self, response):
        inner_news_urls = response.selector.xpath(INNER_LINK_SELECTOR).extract()

        for url in inner_news_urls:
            if url not in self.existing_news_list:
                yield Request(url=url, callback=self.redirect_to_source_url, errback=self.error_in_response)

    def redirect_to_source_url(self, response):
        redirect_url = response.selector.xpath(REDIRECT_LINK_SELECTOR).extract()[0]
        yield Request(
            url=redirect_url,
            method="HEAD",
            callback=self.get_source_news_url,
            errback=self.error_in_response,
            meta={"source_url": response.url},
        )

    def get_source_news_url(self, response):
        item = ArchiveItem()
        item["url"] = response.url
        item["source_url"] = response.meta.get("source_url")
        item["scraping_datetime"] = datetime.now()

        yield item
