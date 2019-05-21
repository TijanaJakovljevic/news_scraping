# -*- coding: utf-8 -*-
BOT_NAME = "scrapers"

SPIDER_MODULES = ["scrapers.news_spiders"]
NEWSPIDER_MODULE = "scrapers.news_spiders"

ROBOTSTXT_OBEY = False

DOWNLOAD_DELAY = 0

DOWNLOADER_MIDDLEWARES = {"libs.common.retry_middleware.CustomRetryMiddleware": 543}

LOG_LEVEL = "INFO"

ITEM_PIPELINES = {"scrapers.pipelines.news_pipeline.NewsPipeline": 300}
