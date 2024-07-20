# meta
BOT_NAME = "llm_scraper"
SPIDER_MODULES = ["llm_scraper.spiders"]
NEWSPIDER_MODULE = "llm_scraper.spiders"

# general settings
LOG_LEVEL = "DEBUG"
ROBOTSTXT_OBEY = False
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_DEBUG = True
HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 0

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
