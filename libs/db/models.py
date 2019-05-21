from datetime import datetime
from mongoengine import StringField, Document, URLField, DateTimeField, ListField, IntField, LongField, BooleanField


class Article(Document):

    internal_id = StringField(max_length=20)
    source_url = URLField(max_length=300)
    url = URLField(required=True, unique=True, max_length=300)
    scraping_datetime = DateTimeField(default=datetime.utcnow)
    title = StringField(max_length=350)
    subtitle = StringField(max_length=150)
    short_description = StringField(max_length=2000)
    article_datetime = DateTimeField()
    category = StringField(max_length=50)
    subcategory = StringField(max_length=50)
    author = StringField(max_length=150)
    image_urls = ListField(StringField(max_length=250))
    tags = ListField(StringField(max_length=100))
    img_number = IntField(min_value=0)
    comment_count = IntField(min_value=0)
    number_of_instagram_links = IntField(min_value=0)
    number_of_twitter_links = IntField(min_value=0)
    number_of_facebook_links = IntField(min_value=0)
    full_article_scraped = BooleanField(default=False)

    meta = {"indexes": ["$url", "article_datetime"]}
