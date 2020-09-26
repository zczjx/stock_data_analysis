#!/usr/bin/env python3
# coding: utf-8

import json
import numpy as np
import pandas as pd
from visdom import Visdom
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.dates as mdate
# import seaborn
# seaborn.set()
# import pylab import mpl
import os, time, sys, pickle
from datetime import datetime
from dateutil.parser import parse

font = {'family': 'SimHei'}

xlabel_dict = {'social_average': u'社会平均', 'state_owned': u'国有单位'}
ylabel_dict = {'salary': u'年收入(RMB)'}

def show_salary_chart(ylabel=''):
    global ylabel_dict
    plt.style.use('seaborn-whitegrid')
    plt.xlabel(u'时间轴', fontproperties='SimHei')
    plt.xticks(rotation=-90)
    plt.title(ylabel, fontproperties='SimHei')
    # plt.xlim(2000, 2020)
    # plt.ylim(-1, max_pe+10)
    plt.legend(loc=0, prop=font)
    plt.grid(True)
    viz = Visdom(env='main')
    viz.matplot(plt)

if __name__=='__main__':
    if len(sys.argv) < 2:
        print("please enter the csv path")
        raise SystemExit(1)

    csv_data_file = sys.argv[1]
    data_frame = pd.read_csv(csv_data_file)
    date_list = data_frame['year'].apply(str).apply(parse)
    print(date_list)
    col = data_frame.columns

    for i in range(1, len(col)):
        print(i, ':', col[i])

    # 社会平均
    data_array = np.array(data_frame[xlabel_dict['social_average']])
    salary_data_series = pd.Series(data_array, index=date_list.values).sort_index(ascending=False)
    plt.plot(salary_data_series.index, salary_data_series.values, label=xlabel_dict['social_average'])

    # 国有单位
    data_array = np.array(data_frame[xlabel_dict['state_owned']])
    salary_data_series = pd.Series(data_array, index=date_list.values).sort_index(ascending=False)
    plt.plot(salary_data_series.index, salary_data_series.values, label=xlabel_dict['state_owned'])
    plt.xticks(salary_data_series.index)

    show_salary_chart(ylabel=ylabel_dict['salary'])

