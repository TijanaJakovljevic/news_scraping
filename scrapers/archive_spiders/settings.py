BOT_NAME = "scrapers"

SPIDER_MODULES = ["scrapers.archive_spiders"]
NEWSPIDER_MODULE = "scrapers.archive_spiders"

ROBOTSTXT_OBEY = True

DOWNLOAD_DELAY = 0

LOG_LEVEL = "INFO"

DOWNLOADER_MIDDLEWARES = {"libs.common.retry_middleware.CustomRetryMiddleware": 543}

ITEM_PIPELINES = {"scrapers.pipelines.archive_pipeline.ArchivePipeline": 300}
