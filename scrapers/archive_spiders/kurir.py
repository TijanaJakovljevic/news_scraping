# -*- coding: utf-8 -*-
import logging
import os

from scrapy import Request, Selector

from libs.common.spider import BaseSpider, ArchiveItem
from libs.config.spiders.kurir_scraper_config import (
    KURIR_ARCHIVE_SPIDER_NAME,
    KURIR_ALLOWED_DOMAINS,
    KURIR_ARCHIVE_SPIDER_BASE_URL,
    LAST_PAGE_SELECTOR,
    ARTICLE_LIST_SELECTOR,
    TITLE_SELECTOR,
    URL_PATH_SELECTOR,
    START_DATE,
    END_DATE,
    KURIR_BASE_URL,
)
from libs.db.client import connect_to_database

log = logging.getLogger(__name__)
dir_path = os.path.dirname(__file__)


class KurirArchiveSpider(BaseSpider):
    name = KURIR_ARCHIVE_SPIDER_NAME
    allowed_domains = KURIR_ALLOWED_DOMAINS
    base_url = KURIR_ARCHIVE_SPIDER_BASE_URL

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.spider_path = dir_path
        connect_to_database()

    def start_requests(self):
        for single_date in BaseSpider.daterange(START_DATE, END_DATE):
            url = self.base_url.format(date=single_date.strftime("%Y-%m-%d"), page=100)

            yield Request(
                url=url,
                callback=self.get_archive_pages,
                errback=self.error_in_response,
                meta={"date_scraping": single_date},
            )

        failed_urls = self.get_failed_urls()
        self.clear_failed_urls_file()

        for url in failed_urls:
            yield Request(url=url, callback=self.parse, errback=self.error_in_response)

    def get_archive_pages(self, response):
        last_page = Selector(response=response).xpath(LAST_PAGE_SELECTOR).extract()[-1]
        urls = self.build_paged_archive_urls(response.meta["date_scraping"], last_page)
        for url in urls:
            yield Request(url=url, callback=self.parse, meta={"source_url": url})

    def parse(self, response):
        articles = response.selector.xpath(ARTICLE_LIST_SELECTOR)
        log.info(f"Received response from {response.url}")

        for article in articles:
            title = article.xpath(TITLE_SELECTOR).extract_first()
            url_path = article.xpath(URL_PATH_SELECTOR).extract_first()
            url = f"{KURIR_BASE_URL}{url_path}"

            item = ArchiveItem()
            item["url"] = url
            item["title"] = title

            yield item

    def build_initial_archivle_urls(self):
        return [
            self.base_url.format(date=single_date.strftime("%Y-%m-%d"), page=100)
            for single_date in KurirArchiveSpider.daterange(START_DATE, END_DATE)
        ]

    def build_paged_archive_urls(self, date_scraping, last_page):
        return [self.base_url.format(date=date_scraping, page=page_number) for page_number in range(1, int(last_page))]
