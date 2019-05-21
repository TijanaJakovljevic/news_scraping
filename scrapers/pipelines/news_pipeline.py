# -*- coding: utf-8 -*-
from libs.db.client import connect_to_database
from libs.db.models import Article


class NewsPipeline(object):
    def __init__(self):
        connect_to_database()

    def process_item(self, item, spider):
        article = Article.objects(url=item.get("url")).first()
        if not article:
            article = Article()

        article.url = item.get("url")
        article.scraping_datetime = item.get("scraping_datetime")
        article.title = item.get("title")
        article.short_description = item.get("short_description")[:2000]
        article.article_datetime = item.get("article_datetime")
        article.category = item.get("category")
        article.subcategory = item.get("subcategory")
        article.author = item.get("author")
        article.tags = item.get("tags")
        article.image_urls = item.get("image_urls")
        article.img_number = item.get("img_number")
        article.comment_count = item.get("comment_count")
        article.number_of_instagram_links = item.get("number_of_instagram_links")
        article.number_of_twitter_links = item.get("number_of_twitter_links")
        article.number_of_facebook_links = item.get("number_of_facebook_links")
        article.full_article_scraped = True
        article.save()

        return item
