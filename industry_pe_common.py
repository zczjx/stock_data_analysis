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
from dateutil.parser import parse

deprecated_date_list = ['2016-08-15']
font = {'family': 'SimHei'}
default_dateset_path = './stock_scrapy/data_collect/industry_pe_history/'
titles = {'1': u'静态市盈率均值', '2': u'静态市盈率中位数',
          '3': u'动态市盈率均值', '4': u'动态市盈率中位数'}
pe_options = {'1': 'static_pe_average', '2': 'static_pe_median',
              '3': 'dynamic_pe_average', '4': 'dynamic_pe_median'}

def filter_exception_date_in_series(data_series):
    # drop deprecated date index
    for date in deprecated_date_list:
        data_series = data_series.drop(parse(date))

    data_series = data_series.dropna()
    return data_series

def show_pe_chart(max_pe=150, pe_key='3'):
    plt.style.use('seaborn-whitegrid')
    plt.ylabel(u'市盈率', fontproperties='SimHei')
    plt.xlabel(u'时间轴', fontproperties='SimHei')
    plt.title(titles[pe_key], fontproperties='SimHei')
    plt.ylim(-1, max_pe+10)
    plt.legend(loc=0, prop=font)
    plt.grid(True)
    viz = Visdom(env='main')
    viz.matplot(plt)



