# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class StockScrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    num = scrapy.Field()
    industry_code = scrapy.Field()
    industry_name = scrapy.Field()
    date = scrapy.Field()
    company_count = scrapy.Field()
    static_pe_average = scrapy.Field()
    static_pe_median = scrapy.Field()
    dynamic_pe_average = scrapy.Field()
    dynamic_pe_median = scrapy.Field()