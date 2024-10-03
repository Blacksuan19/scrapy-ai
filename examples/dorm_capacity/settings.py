from os import environ

# meta
BOT_NAME = "dorm_capacity"
SPIDER_MODULES = ["dorm_capacity.spiders"]
NEWSPIDER_MODULE = "dorm_capacity.spiders"

# general settings
LOG_LEVEL = "DEBUG"
ROBOTSTXT_OBEY = False
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_DEBUG = True
HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 0

# LLM middleware config
LLM_API_BASE = environ.get("LLM_API_BASE")
LLM_UNWRAP_NESTED = True
LLM_MODEL = "gpt-4o-mini"

# download settings
DOWNLOADER_MIDDLEWARES = {"scrapy_llm.handler.LlmExtractorMiddleware": 543}

# saving results to a file with the name of the spider
FEEDS = {
    "results/%(name)s.jsonl": {
        "format": "jsonl",
        "indent": 4,
        "overwrite": True,
    }
}

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
