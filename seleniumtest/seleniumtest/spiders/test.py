# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from pyquery import PyQuery as pq
import time
from ..items import *
import math
import re


class TestSpider(scrapy.Spider):
    name = 'test'
    allowed_domains = ['qixin.com']
    # start_urls = ['http://www.qixin.com/company/9eda1ceb-4d50-4b02-9ef0-ad1437d24f75']
    start_urls = ['http://www.qixin.com/company/518b125f-7f56-4ede-93d1-20e4748d1af8']  #茅台
    options = Options()
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)
    max_depth = 3

    def start_requests(self):
        self.driver.get('http://www.qixin.com/auth/login')
        login(self.driver)
        url = 'http://www.qixin.com/company/518b125f-7f56-4ede-93d1-20e4748d1af8'
        self.cookies = self.driver.get_cookies()
        # print(self.cookies)
        yield scrapy.Request(url, meta={'depth': 0}, cookies=self.cookies, dont_filter=True)

    def parse(self, response):
        check(response, self.driver)

        # 爬基本信息
        # print(response)
        # if response.status != 200:
        #     print(response.text)
        icinfo = response.css('#icinfo')
        company_key = icinfo.xpath('.//tr[1]/td[2]/text()').extract_first()
        print('统一社会信用代码: ', company_key)
        # 统一社会信用代码不存在，放弃爬取
        if company_key is None or len(company_key) < 7:
            print('统一社会信用代码不存在')
            return None
        print('开始爬取工商信息')
        company_item = CompanyItem()
        # 将统一社会信用代码作为公司的_key
        company_item['_id'] = company_key
        company_item['_key'] = company_key
        company_item['name'] = icinfo.xpath(
            '/html/body/div[3]/div/div/div[2]/div/div[1]/h3/text()').extract_first()
        company_item['credit_code'] = icinfo.xpath('.//tr[1]/td[2]/text()').extract_first()
        company_item['organization_code'] = icinfo.xpath('.//tr[1]/td[4]/text()').extract_first()
        company_item['registration_number'] = icinfo.xpath('.//tr[2]/td[2]/text()').extract_first()
        company_item['operning_state'] = icinfo.xpath('.//tr[2]/td[4]/text()').extract_first()
        company_item['industry'] = icinfo.xpath('.//tr[3]/td[2]/text()').extract_first()
        company_item['establishment_date'] = qxb_num(icinfo.xpath('.//tr[3]/td[4]/text()').extract_first())
        company_item['company_type'] = icinfo.xpath('.//tr[4]/td[2]/text()').extract_first()
        company_item['business_term'] = icinfo.xpath('.//tr[4]/td[4]/text()').extract_first()
        company_item['legal_man'] = icinfo.xpath('.//tr[5]/td[2]/a[1]/text()').extract_first()
        company_item['registered_capital'] = qxb_num(icinfo.xpath('.//tr[6]/td[2]/text()').extract_first())
        company_item['registration_authority'] = icinfo.xpath('.//tr[6]/td[4]/text()').extract_first()
        company_item['company_address'] = icinfo.xpath('.//tr[7]/td[2]/text()').extract_first()
        company_item['business_scope'] = icinfo.xpath('.//tr[8]/td[2]/text()').extract_first()

        # if '_investment_key' in response.meta:
        #     company_item['_investment_key'] = response.meta['_investment_key']
        # if '_executive_key' in response.meta:
        #     company_item['_executive_key'] = response.meta['_executive_key']
        # if '_shareholder_key' in response.meta:
        #     company_item['_shareholder_key'] = response.meta['_shareholder_key']
        # # 限制爬取深度
        if response.meta['depth'] > 0:
            s_item = RelationItem()
            if 's_key' in response.meta:
                s_item['from_key'] = company_key
                s_item['to_key'] = response.meta['s_key']
            if 'i_key' in response.meta:
                s_item['from_key'] = response.meta['i_key']
                s_item['to_key'] = company_key
            s_item['name'] = '投资'
            yield s_item
        if response.meta['depth'] > self.max_depth:
            yield company_item
            return None

        time.sleep(1)
        list_href = response.xpath('//a[contains(text(),"上市信息")]/@href').extract_first()
        if list_href:
            ## 爬取上市信息---Done
            list_url = response.urljoin(list_href)
            yield scrapy.Request(list_url, meta={'company_item': company_item,
                                                 'company_key': company_key, 'depth': response.meta['depth']},
                                 cookies=self.cookies, callback=self.parse_list_info,
                                 dont_filter=True)
        else:
            # 上市信息不存在
            yield company_item
            # 主要人员
            print('爬取主要人员')
            employees = response.css('#employees').xpath('.//a[@data-event-name="主要人员-点击名字"]')
            num = 0
            # executive_key_list = []
            for employee in employees:
                executive_key = company_key + '_e' + str(num)
                post = employee.xpath('../preceding-sibling::td[1]/text()').extract_first()
                if len(post) < 2:
                    num = num + 1
                    continue
                executive_item = PersonItem()
                executive_item['_id'] = executive_key
                executive_item['_key'] = executive_key
                executive_item['post'] = post
                executive_item['href'] = employee.xpath('./@href').extract_first()
                executive_item['name'] = employee.xpath('./text()').extract_first()
                yield executive_item
                num = num + 1
                # executive_key_list.append(executive_key)
                # 存储公司-高管关系表
                e_item = RelationItem()
                # e_item['_id'] = company_key
                e_item['to_key'] = company_key
                e_item['from_key'] = executive_key
                e_item['name'] = post
                yield e_item

        # 爬对外投资
        time.sleep(1)
        investment_btn = response.xpath('//a[contains(text(),"对外投资")]/../@class').extract_first()
        if investment_btn != 'disable':
            print('开始爬取对外投资信息')
            # 跳转到对外投资页面
            investment_href = response.xpath('//a[contains(text(),"对外投资")]/@href').extract_first()
            investment_url = response.urljoin(investment_href)
            yield scrapy.Request(investment_url, meta={'company_key': company_key, 'depth': response.meta['depth']},
                                 callback=self.parse_investments, cookies=self.cookies, dont_filter=True)

    # 爬对外投资
    def parse_investments(self, response):
        check(response, self.driver)

        company_key = response.meta['company_key']
        total_num = int(response.css(
            'body > div.container > div > div.col-md-18 > div.tab-content > div.clearfix.margin-t-2x > h4 > span::text').extract_first())
        investment_key_list = []
        num = 0
        try:
            # 第一页
            list = response.css('.app-investment-list .investment-item')
            for li in list:
                href = li.css('.col-2 h5 a::attr(href)').extract_first()
                name = li.css('.col-2 h5 a::text').extract_first()
                print(response.meta['depth'], '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
                # if response.meta['depth'] < self.max_depth:
                    # # 进入被投资公司获取key
                    # print(name)
                    # investment_link = self.wait.until(
                    #     EC.element_to_be_clickable((By.XPATH,'//a[contains(@href, "{}")]'.format(href))))
                    # k = get_key(investment_link, self.driver)
                    # if k == 0:
                    #     continue
                    # else:
                    #     investment_key = k
                    #     investment_item = InvestmentsItem()
                    #     investment_item['_id'] = investment_key
                    #     investment_item['_key'] = investment_key
                    #     investment_item['company_name'] = name
                    #     investment_item['href'] = href
                    #     yield investment_item
                    # num = num + 1
                    # investment_key_list.append(investment_key)
                yield scrapy.Request(response.urljoin(href),
                                    meta={'depth': response.meta['depth'] + 1, 'i_key': company_key},
                                    dont_filter=True, cookies=self.cookies)
                # else:
                #     investment_key = company_key + '_i' + str(num)
                #     company_item = CompanyItem()
                #     company_item['_id'] = investment_key
                #     company_item['_key'] = investment_key
                #     company_item['name'] = name
                #     yield company_item
                #     i_item = RelationItem()
                #     i_item['from_key'] = company_key
                #     i_item['to_key'] = investment_key
                #     i_item['name'] = '投资'
                #     yield i_item
                #     num = num + 1
                    # investment_key_list.append(investment_key)

            # 其他页
            if total_num > 10:
                total_page = math.ceil(total_num / 10)
                self.driver.get(response.url)
                time.sleep(1)
                # 翻页
                for i in range(0, total_page - 1):
                    pagination = self.wait.until(
                        EC.presence_of_element_located((By.CLASS_NAME, 'pagination')))
                    self.driver.execute_script("arguments[0].scrollIntoView(false);", pagination)
                    next = self.wait.until(EC.presence_of_element_located(
                        (By.XPATH, '//ul[@class="pagination"]//li[@class="active"]/following-sibling::li[1]/a')))
                    next.click()
                    time.sleep(1)
                    doc = pq(self.driver.page_source)
                    items = doc('.app-investment-list .investment-item').items()
                    list = self.wait.until(
                        EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.app-investment-list .investment-item')))
                    for li in items:
                        # investment_key = company_key + '_i' + str(num)
                        href = li.find('.h5').children().attr('href')
                        name = li.find('.h5').text()
                        print(response.meta['depth'], '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
                        # if response.meta['depth'] < self.max_depth:
                            #     # 进入被投资公司获取key
                            #     investment_link = self.wait.until(
                            #         EC.element_to_be_clickable((By.XPATH, '//a[contains(@href, "{}")]'.format(href))))
                            #     k = get_key(investment_link, self.driver)
                            #     if k == 0:
                            #         continue
                            #     else:
                            #         investment_key = k
                            #     investment_item = InvestmentsItem()
                            #     investment_item['_id'] = investment_key
                            #     investment_item['_key'] = investment_key
                            #     investment_item['company_name'] = name
                            #     investment_item['href'] = href
                            #     yield investment_item
                            #     num = num + 1
                            #     investment_key_list.append(investment_key)
                        yield scrapy.Request(response.urljoin(href),
                                            meta={'depth': response.meta['depth'] + 1, 'i_key': company_key},
                                            dont_filter=True, cookies=self.cookies)
                        # else:
                        #     investment_key = company_key + '_i' + str(num)
                        #     company_item = CompanyItem()
                        #     company_item['_id'] = investment_key
                        #     company_item['_key'] = investment_key
                        #     company_item['name'] = name
                        #     yield company_item
                        #     i_item = RelationItem()
                        #     i_item['from_key'] = company_key
                        #     i_item['to_key'] = investment_key
                        #     i_item['name'] = '投资'
                        #     yield i_item
                        #     num = num + 1
                            # investment_key_list.append(investment_key)

        except TimeoutException:
            print("Timeout!")
        # finally:
        #     c_i_item = CompanyInvestmentsItem()
        #     c_i_item['_id'] = company_key
        #     c_i_item['company_key'] = company_key
        #     c_i_item['investment_key'] = investment_key_list
        #     yield c_i_item

    # 爬取上市信息
    def parse_list_info(self, response):
        check(response, self.driver)

        company_key = response.meta['company_key']

        # 爬取企业概况
        print('开始爬取企业概况')
        company_item = response.meta['company_item']
        company_item['company_en_name'] = response.xpath(
            '//*[@id="overview"]/table/tbody/tr[1]/td[4]/text()').extract_first()
        company_item['chairman'] = response.xpath('//*[@id="overview"]/table/tbody/tr[2]/td[2]/text()').extract_first()
        # company_item['build_date'] = response.xpath(
        #     '//*[@id="overview"]/table/tbody/tr[4]/td[2]/text()').extract_first()
        company_item['list_date'] = response.xpath('//*[@id="overview"]/table/tbody/tr[4]/td[4]/text()').extract_first()
        company_item['registered_address'] = response.xpath(
            '//*[@id="overview"]/table/tbody/tr[8]/td[2]/text()').extract_first()
        company_item['office_address'] = response.xpath(
            '//*[@id="overview"]/table/tbody/tr[9]/td[2]/text()').extract_first()
        company_item['phone'] = response.xpath('//*[@id="overview"]/table/tbody/tr[10]/td[2]/text()').extract_first()
        company_item['email'] = response.xpath('//*[@id="overview"]/table/tbody/tr[10]/td[4]/text()').extract_first()
        company_item['website'] = response.xpath('//*[@id="overview"]/table/tbody/tr[11]/td[2]/text()').extract_first()
        company_item['fax'] = response.xpath('//*[@id="overview"]/table/tbody/tr[11]/td[4]/text()').extract_first()
        company_item['brief'] = response.xpath('//*[@id="overview"]/table/tbody/tr[12]/td[2]/text()').extract_first()
        yield company_item

        # 爬取十大股东
        # self.driver.get(response.url)
        print('开始爬取十大股东')
        # shareholders_key_list = []
        for i in range(10):
            shareholders_key = company_key + '_s' + str(i)
            href = response.xpath('//*[@id="partners"]/table/tbody/tr[$n]/td[2]/a/@href', n=45 + i * 4).extract_first()
            if href is None:
                continue
            name = response.xpath('//*[@id="partners"]/table/tbody/tr[$n]/td[2]//text()', n=45 + i * 4).extract_first()
            # shareholders_item['name'] = name
            # shareholders_item['href'] = href
            # shareholders_item['sock_type'] = response.xpath('//*[@id="partners"]/table/tbody/tr[$n]/td[2]/text()', n=46+i*4).extract_first()
            # shareholders_item['sock_number'] = response.xpath('//*[@id="partners"]/table/tbody/tr[$n]/td[4]/text()', n=46+i*4).extract_first()
            # shareholders_item['sock_rate'] = response.xpath('//*[@id="partners"]/table/tbody/tr[$n]/td[2]/text()', n=47+i*4).extract_first()
            # shareholders_item['sock_change'] = response.xpath('//*[@id="partners"]/table/tbody/tr[$n]/td[4]/text()', n=47+i*4).extract_first()
            # shareholders_item['change_rate'] = response.xpath('//*[@id="partners"]/table/tbody/tr[$n]/td[2]/text()', n=48+i*4).extract_first()
            print(response.meta['depth'], '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
            if re.search('name-detail', href):
                # 人
                # shareholders_item = ShareholdersItem()
                # shareholders_item['_id'] = shareholders_key
                # shareholders_item['_key'] = shareholders_key
                man = PersonItem()
                man['name'] = name
                man['_key'] = shareholders_key
                man['_id'] = shareholders_key
                yield man
                # yield shareholders_item
                s_item = RelationItem()
                s_item['from_key'] = shareholders_key
                s_item['to_key'] = company_key
                s_item['name'] = '投资'
                yield s_item
                # shareholders_key_list.append(shareholders_key)
            else:
                # if response.meta['depth'] < self.max_depth:
                    # 公司
                    # link = self.wait.until(
                    #     EC.element_to_be_clickable((By.XPATH,
                    #     '//*[@id="partners"]/table/tbody//a[contains(@href, "{}")]'.format(href))))
                    # k = get_key(link, self.driver)
                    # if k == 0:
                    #     continue
                    # else:
                    #     shareholders_key = k
                    #     shareholders_item['_id'] = shareholders_key
                    #     shareholders_item['_key'] = shareholders_key
                    #     yield shareholders_item
                    #     shareholders_key_list.append(shareholders_key)
                    # 爬取下一级公司
                print('爬取下一级公司')
                yield scrapy.Request(response.urljoin(href),
                                    meta={'depth': response.meta['depth'] + 1, 's_key': company_key},
                                    callback=self.parse, dont_filter=True, cookies=self.cookies)
                # else:
                #     # shareholders_item['_id'] = shareholders_key
                #     # shareholders_item['_key'] = shareholders_key
                #     # yield shareholders_item
                #     # shareholders_key_list.append(shareholders_key)
                #     company_item = CompanyItem()
                #     company_item['_id'] = shareholders_key
                #     company_item['_key'] = shareholders_key
                #     company_item['name'] = name
                #     yield company_item
                #     s_item = RelationItem()
                #     s_item['from_key'] = shareholders_key
                #     s_item['to_key'] = company_key
                #     s_item['name'] = '投资'
                #     yield s_item

        # # 存储公司-股东关系表
        # c_s_item = RelationItem()
        # # c_s_item['_id'] = company_key
        # c_s_item['to_key'] = company_key
        # c_s_item['from_key'] = shareholders_key_list
        # yield c_s_item

        # 高管信息
        print('开始爬取高管信息')
        names = response.css('#newOTCEmployees table tbody').xpath('.//td[contains(text(),"姓名")]')
        # executive_key_list = []
        id = 0
        for name in names:
            post = name.xpath('../following-sibling::tr[1]/td[2]/text()').extract_first()
            if len(post) < 2:
                continue
            executive_item = PersonItem()
            executive_key = company_key + '_e' + str(id)
            executive_item['_id'] = executive_key
            executive_item['_key'] = executive_key
            executive_item['post'] = post
            executive_item['name'] = name.xpath('./following-sibling::td/a[1]/text()').extract_first()
            executive_item['href'] = name.xpath('./following-sibling::td/a[1]/@href').extract_first()
            executive_item['age'] = name.xpath('../following-sibling::tr[1]/td[4]/text()').extract_first()
            executive_item['education'] = name.xpath('../following-sibling::tr[2]/td[2]/text()').extract_first()
            executive_item['appointment_date'] = name.xpath(
                '../following-sibling::tr[2]/td[4]/text()').extract_first()
            yield executive_item
            e_item = RelationItem()
            e_item['to_key'] = company_key
            e_item['from_key'] = executive_key
            e_item['name'] = post
            id = id + 1
            # executive_key_list.append(executive_key)
            # # 存储公司-高管关系表
            # c_e_item = RelationItem()
            # # c_e_item['_id'] = company_key
            # c_e_item['from_key'] = company_key
            # c_e_item['to_key'] = executive_key_list
            # yield c_e_item


def get_key(link, driver):
    try:
        driver.execute_script("arguments[0].scrollIntoView(false);", link)
        link.click()
        windows = driver.window_handles
        driver.switch_to.window(windows[-1])
        if len(driver.find_elements_by_class_name('error-500')) > 0:
            # error-500
            driver.refresh()
        if len(driver.find_elements_by_class_name('error-403')) > 0:
            # 403
            # self.driver.get(response.url)
            print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~403~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
            btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
                (By.XPATH, '/html/body/div[3]/div/div/div/div/button')))
            btn.click()
            time.sleep(2)
        key = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="icinfo"]/table/tbody/tr[1]/td[2]')))
        if len(key.text) < 7:
            print('统一社会信用代码不存在')
            driver.close()
            driver.switch_to.window(windows[0])
            return 0
        else:
            key = key.text
        driver.close()
        driver.switch_to.window(windows[0])
        return key
    except TimeoutException:
        print('Timeout!')
        driver.close()
        driver.switch_to.window(windows[0])
        return 0


def qxb_num(str):
    map = {
        '0': '7',
        '1': '3',
        '2': '6',
        '3': '1',
        '4': '0',
        '5': '8',
        '6': '2',
        '7': '5',
        '8': '4'
    }
    a = ''
    for i in str:
        i = map.get(i, i)
        a = a + i
    return a

def check(response, driver):
    wait = WebDriverWait(driver, 10)
    if response.status == 302:
        driver.get(response.url)
        if re.search('login', driver.current_url):
            login(driver)
    # error-container error-500
    if response.status == 403:
        driver.get(response.url)
        time.sleep(1)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(),"点击按钮进行验证")]'))).click()
        time.sleep(8)
    if response.status == 500:
        driver.get(response.url)
        driver.refresh()
        time.sleep(2)

def login(driver):
    try:
        wait = WebDriverWait(driver, 10)
        username = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'input-flat-user')))
        password = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'input-flat-lock')))
        submit = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'btn-block')))
        username.send_keys('13531617086')
        password.send_keys('123')
        submit.click()
        time.sleep(1)
    except TimeoutException:
        print('Timeout!')


