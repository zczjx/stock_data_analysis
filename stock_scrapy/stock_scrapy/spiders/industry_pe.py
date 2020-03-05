# -*- coding: utf-8 -*-
import scrapy
import json
import os
from stock_scrapy.items import StockScrapyItem


class IndustryPeSpider(scrapy.Spider):
    name = 'industry_pe'
    # allowed_domains = ['http://quotes.money.163.com/hs/marketdata/hybjsyl.html']
    start_urls = ['http://quotes.money.163.com/hs/marketdata/hybjsyl.html']
    custom_settings = {
        'LOG_LEVEL': 'INFO',
        "DEFAULT_REQUEST_HEADERS": {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36'
        }
    }

    def __init__(self):
        self.dir_path = './data_collect/industry_pe_history/'
        self.industry_code_map= {}
        self.date_history_record_list = []
        self.date_record_file_path = self.dir_path + 'date_record.json';
        date_history_exist_flag = os.path.exists(self.date_record_file_path)
        if date_history_exist_flag:
            # will read and update the date record file
            self.date_record_rd_f = open(self.date_record_file_path, 'r+')
            self.date_history_record_list = json.load(self.date_record_rd_f)
            self.date_record_rd_f.close()
            self.date_record_wr_f = open(self.date_record_file_path, 'w+')
        else:
            # will create a new date record file
            self.date_record_wr_f = open(self.date_record_file_path, 'w+')
        # self.industry_code_f = open(self.dir_path + 'industry_code.json', 'r', encoding='utf-8-sig')
        # self.industry_code_map = json.load(self.industry_code_f)
        # print(self.industry_code_map)

    def parse(self, response):
        self.date_list = response.css('.tool-bar').css('option::text').getall()
        api_url_base = 'http://quotes.money.163.com/hs/marketdata/service/hypjsyl.php?query=hycode:5;'
        data_req = 'date:'
        fields = '&fields=NO,TDATE,HY,NUM,PE1_A,PE2_M,PE3_A,PE4_M&sort=INDUSTRYCODE&order=asc&count=1000'
        self.update_list = list(set(self.date_list) - set(self.date_history_record_list))
        self.update_list.sort()
        print('update_list--> ', self.update_list)
        print('total pages:', len(self.update_list))
        for date in self.update_list:
            api_url = api_url_base + data_req + date + fields
            req = scrapy.Request(api_url, callback=self.parse_query_result_json)
            yield req

    def parse_query_result_json(self, response):
        respjson = json.loads(response.body)
        print('get data from: ', response.url)
        for record in respjson.get('list'):
            item = StockScrapyItem()
            # print(record)
            item['num'] = record['NO']
            item['industry_code'] = record['INDUSTRYCODE']
            item['industry_name'] = record['HY']
            item['date'] = record['TDATE']
            item['company_count'] = record['NUM']
            item['static_pe_average'] = record.get('PE1_A')
            item['static_pe_median'] = record.get('PE2_M')
            item['dynamic_pe_average'] = record.get('PE3_A')
            item['dynamic_pe_median'] = record.get('PE4_M')
            # self.industry_code_map[item['industry_code']] = item['industry_name']
            yield item

    def closed(self, reason):
        json.dump(self.date_list, self.date_record_wr_f)
        self.date_record_wr_f.close()
        # json.dump(self.industry_code_map, self.industry_code_f)
        # self.industry_code_f.close()