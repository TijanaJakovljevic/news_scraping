import datetime

VESTI_SPIDER_NAME = "vesti"
VESTI_ALLOWED_DOMAINS = ["vesti.rs"]

BASE_URL_TEMPLATE = "https://www.vesti.rs/arhiva/{year}/{month}/{day}/{source}/"

BLIC = "blic"
VECERNJE_NOVOSTI = "vecernje_novosti"
SOURCES = [BLIC]

START_DATE = datetime.date(2018, 1, 1)
END_DATE = datetime.date(2018, 12, 31)

# selectors
REDIRECT_LINK_SELECTOR = '//p[@class="continue-r"]/a/@href'
INNER_LINK_SELECTOR = '//div[@class="news-inner"]/a/@href'
NUMBER_OF_PAGES_SELECTOR = '//div[@class="pagination"]//a/text()'
