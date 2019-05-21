from datetime import datetime

from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Identity

from scrapers.news_spiders.item_loaders.parsing import lowercase_and_strip, split, to_int

CONFIGURATIONS = [
    {"field": "title", "selector": "//title/text()"},
    {"field": "short_description", "selector": "//meta[@name='description']/@content"},
    {"field": "author", "selector": "//meta[@property='article:author']/@content"},
    {"field": "tags", "selector": "//meta[@name='keywords']/@content"},
    {"field": "category", "selector": "(//header/ul[@class='breadcrumbs']/li/a/text())[2]"},
    {"field": "subcategory", "selector": "(//header/ul[@class='breadcrumbs']/li/a/text())[3]"},
    {"field": "article_datetime", "selector": "//ul[@class='article-info']/li/time/@datetime"},
    {"field": "comment_count", "selector": "//input[@id='forum-comment-number']/@value"},
    {"field": "image_urls", "selector": "//div[@class='article-body']//img/@src"},
    {"field": "img_number", "selector": "count(//div[@class='article-body']//img/@src)"},
    {"field": "number_of_facebook_links", "selector": "count(//div[contains(@class, 'fb-post')])"},
    {"field": "number_of_instagram_links", "selector": "count(//div[contains(@class, 'instagram-media')])"},
    {"field": "number_of_twitter_links", "selector": "count(//div[@class='twitter'])"},
]


def parse_article_date(value):
    date_format = "%d.%m.%Y. %H:%M"
    return datetime.strptime(value, date_format)


class BlicLoader(ItemLoader):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for configuration_item in CONFIGURATIONS:
            self.add_xpath(configuration_item["field"], configuration_item["selector"])

    tags_in = MapCompose(lowercase_and_strip, split)
    category_in = MapCompose(lowercase_and_strip)
    subcategory_in = MapCompose(lowercase_and_strip)
    comment_count_in = MapCompose(to_int)
    img_number_in = MapCompose(to_int)
    number_of_instagram_links_in = MapCompose(to_int)
    number_of_twitter_links_in = MapCompose(to_int)
    number_of_facebook_links_in = MapCompose(to_int)
    article_datetime_in = MapCompose(parse_article_date)

    default_output_processor = TakeFirst()
    tags_out = Identity()
    image_urls_out = Identity()
