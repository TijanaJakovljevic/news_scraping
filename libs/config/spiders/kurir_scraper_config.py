import datetime

KURIR_NEWS_SPIDER_NAME = "kurir_news"
KURIR_ARCHIVE_SPIDER_NAME = "kurir_archive"
KURIR_ALLOWED_DOMAINS = ["kurir.rs"]

KURIR_ARCHIVE_SPIDER_BASE_URL = "https://www.kurir.rs/arhiva/{date}/strana/{page}"
KURIR_BASE_URL= "https://www.kurir.rs"
START_DATE = datetime.date(2018, 1, 1)
END_DATE = datetime.date(2018, 2, 1)

# selectors
# archive
TITLE_SELECTOR = ".//div[contains(@class, 'title')]/h2/text()"
ARTICLE_LIST_SELECTOR = "//div[contains(@class, 'mainNewsBlockWrap blockFull')]//a[contains(@class, 'itemLnk')]"
LAST_PAGE_SELECTOR = '//div[contains(@class, "pagination")]//a/text()'
URL_PATH_SELECTOR = ".//@href"

# news
COMMENT_REGEX = ".*?Komentari \((\d+?)\)"
COMMENT_SELECTOR = "https://www.kurir.rs/ajax/get-tpl?id=7&type=comments_preview&content_id={}"
