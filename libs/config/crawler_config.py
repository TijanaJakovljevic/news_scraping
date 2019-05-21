from libs.config.spiders.blic_scraper_config import BLIC_SPIDER_NAME
from libs.config.spiders.kurir_scraper_config import KURIR_ARCHIVE_SPIDER_NAME, KURIR_NEWS_SPIDER_NAME
from libs.config.spiders.novosti_scraper_config import NOVOSTI_SPIDER_NAME
from libs.config.spiders.vesti_scraper_config import VESTI_SPIDER_NAME

CRAWLER_CONFIG = {
    VESTI_SPIDER_NAME: "scrapers.archive_spiders.settings",
    KURIR_ARCHIVE_SPIDER_NAME: "scrapers.archive_spiders.settings",
    KURIR_NEWS_SPIDER_NAME: "scrapers.news_spiders.settings",
    BLIC_SPIDER_NAME: "scrapers.news_spiders.settings",
    NOVOSTI_SPIDER_NAME: "scrapers.news_spiders.settings",
}
