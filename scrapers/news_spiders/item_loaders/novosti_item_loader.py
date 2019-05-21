from datetime import datetime

from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Identity

from scrapers.news_spiders.item_loaders.parsing import to_int

configuration = [
    {"field": "title", "selector": "//title/text()"},
    {"field": "short_description", "selector": "//meta[@name='description']/@content"},
    {"field": "author", "selector": "//div[@class='grid_16']//div[@class='articleInfo']/span/text()"},
    {"field": "tags", "selector": "//meta[@name='keywords']/@content"},
    {"field": "category", "selector": "(//div[@class='menuWide']//li[@class='opened']//a/text())[1]"},
    {"field": "subcategory", "selector": "(//div[@class='menuWide']//li[@class='opened']//a/text())[2]"},
    {"field": "article_datetime", "selector": "//meta[contains(@name,'date')]/@value"},
    {"field": "comment_count", "selector": "//div[@class='grid_16']//div[@class='articleInfo']/a/strong/text()"},
    {
        "field": "image_urls",
        "selector": "//div[@class='inlineImage_center']/img/@src|//div[@class='gallery']/div[@class='imgb']/a/img/@src",
    },
    {
        "field": "img_number",
        "selector": "count(//div[@class='inlineImage_center']/img/@src|//div[@class='gallery']/div[@class='imgb']/a/img/@src)",
    },
]


def parse_datetime(value):
    return datetime.fromtimestamp(to_int(value))


def parse_title(value):
    return value.split(" |")[0]


def create_links(value):
    return "novosti.rs" + value


class NovostiLoader(ItemLoader):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for configuration_item in configuration:
            self.add_xpath(configuration_item["field"], configuration_item["selector"])

    title_in = MapCompose(parse_title)
    article_datetime_in = MapCompose(parse_datetime)
    comment_count_in = MapCompose(to_int)
    img_number_in = MapCompose(to_int)
    image_urls_in = MapCompose(create_links)

    default_output_processor = TakeFirst()
    image_urls_out = Identity()
