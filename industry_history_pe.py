#!/usr/bin/env python3
# coding: utf-8

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
from dateutil.parser import parse

deprecated_date_list = ['2016-08-15']
font = {'family': 'SimHei'}

def filter_exception_date_in_series(data_series):
    # drop deprecated date index
    for date in deprecated_date_list:
        data_series = data_series.drop(parse(date))
    return data_series

if __name__=='__main__':
    if len(sys.argv) < 2:
        print("pls enter dataset file path!")
        raise SystemExit(1)

    csv_data_file = sys.argv[1]
    data_frame = pd.read_csv(csv_data_file)
    date_list = data_frame['date'].apply(str).apply(parse)
    name = data_frame['industry_name'][0]
    industry_code = data_frame['industry_code'][0]
    history_count = np.array(data_frame['company_count'])
    static_pe_average = np.array(data_frame['static_pe_average'])
    static_pe_median = np.array(data_frame['static_pe_median'])
    dynamic_pe_average = np.array(data_frame['dynamic_pe_average'])
    dynamic_pe_median = np.array(data_frame['dynamic_pe_median'])
    print(name)
    print(data_frame.index)
    print(data_frame.columns)
    dpa_data_series = pd.Series(dynamic_pe_average, index=date_list.values).sort_index(ascending=False)
    # print('2015-12-25: ', dpa_data_series['2015-12-25'])
    # print('2016-08-15: ', dpa_data_series['2016-08-15'])
    dpa_data_series = filter_exception_date_in_series(data_series=dpa_data_series)
    print(dpa_data_series)
    # print(dpa_data_series[parse('2020-03-06')])
    print(dpa_data_series[parse('2015-12-21')])
    # pe_list = dpa_data_series.tolist()
    # dpa_data_series.plot()
    plt.style.use('seaborn-whitegrid')
    plt.plot(dpa_data_series.index, dpa_data_series.values, color='r', label=industry_code + name)
    plt.ylabel(u'市盈率', fontproperties='SimHei')
    plt.xlabel(u'时间轴', fontproperties='SimHei')
    plt.title(u'动态市盈率均值', fontproperties='SimHei')
    plt.ylim(-1, 150)
    plt.legend(loc=0, prop=font)
    plt.grid(True)
   # plt.hist(dpa_data_series)
   # plt.title('industry history pe')
   # plt.xlabel('date')
   # plt.ylabel('pe')
    viz = Visdom(env='main')
    viz.matplot(plt)


