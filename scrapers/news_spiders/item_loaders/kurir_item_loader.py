# -*- coding: utf-8 -*-
import re
from datetime import datetime

from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose

from scrapers.news_spiders.item_loaders.parsing import lowercase_and_strip, to_int

CONFIGURATION = [
    {"field": "title", "selector": "//h1/text()"},
    {"field": "short_description", "selector": "//h3[@class='preHead']/span/text()"},
    {"field": "author", "selector": "//p[contains(text(), 'Kurir.rs')]"},
    {"field": "author", "selector": "//p/*[contains(text(), 'Kurir.rs')]"},
    {"field": "author", "selector": "//p/*[contains(text(), 'Promo')]"},
    {"field": "author", "selector": "//p[contains(text(), 'Promo')]"},
    {"field": "tags", "selector": "//a[contains(@class, 'lnk')]/text()"},
    {"field": "category", "selector": "//div/strong/text()"},
    {"field": "article_datetime", "selector": "//div[contains(@class, 'artTime fixed')]/span[1]/@content"},
    {"field": "article_id", "selector": "//div[@class='articleNav']/@data-id"},
    {"field": "img_number", "selector": "count(//figure[contains(@class, 'elWrap imgFull')]/img/@src)"},
    {"field": "image_urls", "selector": "//figure[contains(@class, 'elWrap imgFull')]/img/@src"},
    {"field": "number_of_instagram_links", "selector": "count(//iframe[contains(@id,'instagram-embed')])"},
]


def parse_article_date(value):
    date_format = "%Y-%m-%dT%H:%M"
    return datetime.strptime(value, date_format)


def parse_authors(value):
    if "promo" in value:
        return "promo"
    author = re.match(".*?\(?kurir(?:\.rs)?/?(.*?)(?:/|foto|\))", value)

    return author.group(1).strip("<") if author and author.group(1) else "kurir.rs"


class KurirArticleLoader(ItemLoader):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for configuration_item in CONFIGURATION:
            self.add_xpath(configuration_item["field"], configuration_item["selector"], re=configuration_item.get("re"))

    default_input_processor = MapCompose(lowercase_and_strip)
    author_in = MapCompose(lowercase_and_strip, parse_authors)
    article_datetime_in = MapCompose(parse_article_date)
    img_number_in = MapCompose(to_int)
    number_of_instagram_links_in = MapCompose(to_int)
    number_of_twitter_links_in = MapCompose(to_int)
    number_of_facebook_links_in = MapCompose(to_int)

    default_output_processor = TakeFirst()
    image_urls_out = MapCompose()
    tags_out = MapCompose()
