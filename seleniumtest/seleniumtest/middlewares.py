# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import random
import base64
from fake_useragent import UserAgent
import time
import requests
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

class SeleniumtestSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class SeleniumtestDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        driver = webdriver.Chrome()
        wait = WebDriverWait(driver, 10)
        driver.get(request.url)
        if re.search('login', driver.current_url):
            try:
                username = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'input-flat-user')))
                password = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'input-flat-lock')))
                submit = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'btn-block')))
                username.send_keys('13531617086')
                password.send_keys('123')
                submit.click()
                time.sleep(1)
                cookies = driver.get_cookies()
                request.cookies = cookies
            except TimeoutException:
                print('Timeout!')
            # return HtmlResponse(request.url, encoding="utf-8", request=request, cookies = cookies)
        return request

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

class RandomUserAgent(object):
    """Randomly rotate user agents based on a list of predefined ones"""

    def __init__(self, crawler):
        self.ua = UserAgent()
        self.ua_type = crawler.settings.get("RANDOM_UA_TYPE", "random")

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_request(self, request, spider):
        def get_ua_type():
            return getattr(self.ua, self.ua_type)

        random_useragent = get_ua_type()
        print("**************************", random_useragent)
        request.headers.setdefault('User-Agent', random_useragent)


class ProxyMiddleware(object):
    def process_request(self, request, spider):
        '''对request对象加上proxy'''
        proxy = self.get_random_proxy()
        if proxy:
            print("***********************this is request ip:" + proxy)
            request.meta['proxy'] = proxy
        else:
            return request

    def process_response(self, request, response, spider):
        '''对返回的response处理'''
        # 如果返回的response状态不是200，重新生成当前request对象
        if response.status != 200:
            print(response)
            while 1:
                proxy = self.get_random_proxy()
                if proxy:
                    break
                else:
                    time.sleep(1)
            print("this is response ip:" + proxy)
            # 对当前request加上代理
            request.meta['proxy'] = proxy
            return request
        return response

    def get_random_proxy(self):
        # '''随机从文件中读取proxy'''
        # while 1:
        #     with open('seleniumtest/proxies.txt', 'r') as f:
        #         proxies = f.readlines()
        #     if proxies:
        #         break
        #     else:
        #         time.sleep(1)
        # proxy = random.choice(proxies).strip()
        # return proxy
        '''从代理池中获取proxy'''
        try:
            response = requests.get('http://127.0.0.1:5555/random')
            if response.status_code == 200:
                proxy = 'http://' + response.text
                return proxy
            return None
        except ConnectionError:
            return None
