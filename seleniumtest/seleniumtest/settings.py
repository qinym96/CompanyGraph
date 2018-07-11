# -*- coding: utf-8 -*-

# Scrapy settings for seleniumtest project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'seleniumtest'

SPIDER_MODULES = ['seleniumtest.spiders']
NEWSPIDER_MODULE = 'seleniumtest.spiders'


FEED_EXPORT_ENCONDING = 'utf-8'

MONGO_URI = 'localhost'
MONGO_DB = 'Maotai2'

RANDOM_UA_TYPE = 'chrome'
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'seleniumtest (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 1

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 8
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# crawler
# CRAWLERA_ENABLED = True
# CRAWLERA_USER = '31749bc973a0498dac99dd07dc64dcb9:'
# CRAWLERA_PASS = ''
# CRAWLERA_PRESERVE_DELAY = True

# DOWNLOAD_TIMEOUT = 60

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    'Connection': 'keep - alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    "Accept-Encoding": "gzip, deflate, br",
    'Host': 'www.qixin.com',
    "Upgrade-Insecure-Requests": "1",
}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'seleniumtest.middlewares.SeleniumtestSpiderMiddleware': 543,
#}

# RetryMiddleware
RETRY_ENABLED: True
RETRY_TIMES: 5
# RETRY_HTTP_CODECS:

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   'seleniumtest.middlewares.SeleniumtestDownloaderMiddleware': None,
    # 'scrapy.downloadermiddlewares.retry.RetryMiddleware': 555,
    'seleniumtest.middlewares.RandomUserAgent': 600,
    # 'seleniumtest.middlewares.ProxyMiddleware': 700,
    # 'scrapy_crawlera.CrawleraMiddleware': 700
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'seleniumtest.pipelines.SeleniumtestPipeline': 300,
    'seleniumtest.pipelines.MongoPipeline': 400,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = False
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
HTTPERROR_ALLOWED_CODES = [403, 500, 302]