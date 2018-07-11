# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SeleniumtestItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class CompanyItem(scrapy.Item):
    # company_info = scrapy.Field()
    # 工商信息
    _id = scrapy.Field()
    _key = scrapy.Field()
    name = scrapy.Field()
    credit_code = scrapy.Field()
    organization_code = scrapy.Field()
    registration_number = scrapy.Field()
    operning_state = scrapy.Field()
    industry = scrapy.Field()
    establishment_date = scrapy.Field()
    company_type = scrapy.Field()
    business_term = scrapy.Field()
    legal_man = scrapy.Field()
    registered_capital = scrapy.Field()
    registration_authority = scrapy.Field()
    company_address = scrapy.Field()
    business_scope = scrapy.Field()
    # 上市信息
    company_en_name = scrapy.Field()
    chairman = scrapy.Field()
    build_date = scrapy.Field()
    list_date = scrapy.Field()
    registered_address = scrapy.Field()
    office_address = scrapy.Field()
    phone = scrapy.Field()
    email = scrapy.Field()
    website = scrapy.Field()
    fax = scrapy.Field()
    brief = scrapy.Field()

    shareholders = scrapy.Field()
    executive = scrapy.Field()

    _investment_key = scrapy.Field() # 被投资
    _executive_key = scrapy.Field() # 被任职
    _shareholder_key = scrapy.Field() # 投资

class InvestmentsItem(scrapy.Item):
    # investments = scrapy.Field()
    # _id = scrapy.Field()
    # _key = scrapy.Field()
    _id = scrapy.Field()
    _key = scrapy.Field()
    company_name = scrapy.Field()
    href = scrapy.Field()

class PersonItem(scrapy.Item):
    # executive_info = scrapy.Field()
    _id = scrapy.Field()
    _key = scrapy.Field()
    name = scrapy.Field()
    href = scrapy.Field()
    post = scrapy.Field()
    age = scrapy.Field()
    education = scrapy.Field()
    appointment_date = scrapy.Field()

class ShareholdersItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # shareholders = scrapy.Field()
    _id = scrapy.Field()
    _key = scrapy.Field()
    name = scrapy.Field()
    href = scrapy.Field()
    sock_type = scrapy.Field()
    sock_number = scrapy.Field()
    sock_rate = scrapy.Field()
    sock_change = scrapy.Field()
    change_rate = scrapy.Field()

# class CompanyShareholdersItem(scrapy.Item):
#     _id = scrapy.Field()
#     company_key = scrapy.Field()
#     shareholders_key = scrapy.Field()
#
# class CompanyPersonItem(scrapy.Item):
#     _id = scrapy.Field()
#     company_key = scrapy.Field()
#     executive_key = scrapy.Field()
#
# class CompanyInvestmentsItem(scrapy.Item):
#     _id = scrapy.Field()
#     company_key = scrapy.Field()
#     investment_key = scrapy.Field()

class RelationItem(scrapy.Item):
    from_key = scrapy.Field()
    to_key = scrapy.Field()
    name = scrapy.Field()