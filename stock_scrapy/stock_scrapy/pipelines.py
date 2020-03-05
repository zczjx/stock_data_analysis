# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import csv
import os

class StockScrapyPipeline(object):
    def __init__(self):
        self.dir_path = './data_collect/industry_pe_history/'
        self.file_list = [  'A', 'A01', 'A02', 'A03', 'A04', 'A05',
                            'B', 'B06', 'B07', 'B08', 'B09', 'B10', 'B11',
                            'C', 'C13', 'C14', 'C15', 'C17', 'C18', 'C19',
                            'C20', 'C21', 'C22', 'C23', 'C24', 'C25', 'C26', 'C27', 'C28', 'C29',
                            'C30', 'C31', 'C32', 'C33', 'C34', 'C35', 'C36', 'C37', 'C38', 'C39',
                            'C40', 'C41', 'C42',
                            'D', 'D44', 'D45', 'D46',
                            'E', 'E47', 'E48', 'E49', 'E50',
                            'F', 'F51', 'F52',
                            'G', 'G53', 'G54', 'G55', 'G56', 'G58', 'G59', 'G60',
                            'H', 'H61', 'H62',
                            'I', 'I63', 'I64', 'I65',
                            'J', 'J66', 'J67', 'J68', 'J69',
                            'K', 'K70',
                            'L', 'L71', 'L72',
                            'M', 'M73', 'M74', 'M75',
                            'N', 'N77', 'N78',
                            'O', 'O80',
                            'P', 'P82',
                            'Q', 'Q83',
                            'R', 'R85', 'R86', 'R87', 'R88',
                            'S', 'S90' ]
        self.file_handles_map = {}
    def open_spider(self, spider):
        for file_name in self.file_list:
            full_file_path = self.dir_path + file_name + '.csv'
            file_exist_flag = os.path.exists(full_file_path)
            self.file_handles_map[file_name] = open(full_file_path, 'a+', encoding='utf-8-sig')
            writer = csv.writer(self.file_handles_map[file_name])
            if not file_exist_flag:
                writer.writerow(['date', 'industry_code', 'industry_name',
                                'company_count', 'static_pe_average', 'static_pe_median',
                                'dynamic_pe_average', 'dynamic_pe_median'])

    def close_spider(self, spider):
        for file_name in self.file_list:
            self.file_handles_map[file_name].close()

    def process_item(self, item, spider):
        writer = csv.writer(self.file_handles_map[item['industry_code']])
        writer.writerow([item['date'], item['industry_code'], item['industry_name'],
                         item['company_count'], item['static_pe_average'], item['static_pe_median'],
                         item['dynamic_pe_average'], item['dynamic_pe_median']])
