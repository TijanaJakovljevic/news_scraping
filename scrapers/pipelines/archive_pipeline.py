# -*- coding: utf-8 -*-
from scrapy.exceptions import DropItem

from libs.db.client import connect_to_database
from libs.db.models import Article


class ArchivePipeline(object):
    def __init__(self):
        connect_to_database()

    def process_item(self, item, spider):
        article = Article.objects(url=item.get("url")).first()
        if article:
            raise DropItem("Article already exists")

        article = Article()
        article.url = item.get("url")
        article.title = item.get("title")
        article.source_url = item.get("source_url")
        article.scraping_datetime = item.get("scraping_datetime")
        article.save()

        return item
