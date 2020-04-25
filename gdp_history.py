#!/usr/bin/env python3
# coding: utf-8

import json
import numpy as np
import pandas as pd
from visdom import Visdom
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.dates as mdate
import seaborn
seaborn.set()
# import pylab import mpl
import os, time, sys, pickle
from datetime import datetime
from dateutil.parser import parse


font = {'family': 'SimHei'}
gdp_dataset_file_dict = {
    'amount': 'stock_scrapy/data_collect/gdp/gdp_amount_china.csv',
    'rate': 'stock_scrapy/data_collect/gdp/gdp_growth_rate_china.csv',
}

ylabel_dict = {'amount': u'gdp总额(亿人民币)', 'rate': u'gdp增长(%)'}

def show_gdp_chart(ylabel=''):
    global ylabel_dict
    plt.style.use('seaborn-whitegrid')
    plt.ylabel(ylabel_dict[ylabel], fontproperties='SimHei')
    plt.xlabel(u'时间轴', fontproperties='SimHei')
    plt.title(ylabel_dict[ylabel], fontproperties='SimHei')
    # plt.xlim(2000, 2020)
    # plt.ylim(-1, max_pe+10)
    plt.legend(loc=0, prop=font)
    plt.grid(True)
    viz = Visdom(env='main')
    viz.matplot(plt)

if __name__=='__main__':
    if len(sys.argv) < 2:
        print("please enter [amount | rate] to choose what to show")
        raise SystemExit(1)

    csv_data_file = gdp_dataset_file_dict[sys.argv[1]]
    data_frame = pd.read_csv(csv_data_file)
    date_list = data_frame['year'].apply(str).apply(parse)
    print(date_list)
    col = data_frame.columns

    for i in range(1, len(col)):
        print(i, ':', col[i])

    print('请从以上代码中选择要显示的城市, 用空格键分隔, 忽略大小写: ')
    input_code_list = input().upper().split(' ')
    input_code_list =list(map(int, input_code_list))

    for code in input_code_list:
        data_array = np.array(data_frame[col[code]])
        gdp_data_series = pd.Series(data_array, index=date_list.values).sort_index(ascending=False)
        plt.plot(gdp_data_series.index, gdp_data_series.values, label=col[code])
    show_gdp_chart(ylabel=sys.argv[1])
