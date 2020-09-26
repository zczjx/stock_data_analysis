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

house_price_dict = {'price': u'每平米单价'}
salary_dict = {'social_average': u'社会平均', 'state_owned': u'国有单位'}
xlabel_dict = {'social_ratio': u'房价-社会平均月收入比', 'state_owned_ratio': u'房价-国有单位月收入比'}
ylabel_dict = {'ration': u'房价月收入比'}

def show_ratio_chart(ylabel=''):
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
    if len(sys.argv) < 3:
        print("please enter the house price and annual salary csv path")
        raise SystemExit(1)

    # house price
    csv_data_file = sys.argv[1]
    house_data_frame = pd.read_csv(csv_data_file)
    house_date_list = house_data_frame['year'].apply(str).apply(parse)
    data_array = np.array(house_data_frame[house_price_dict['price']])
    house_price = pd.Series(data_array, index=house_date_list.values).sort_index(ascending=True)

    # annual salary
    csv_data_file = sys.argv[2]
    salary_data_frame = pd.read_csv(csv_data_file)
    salary_date_list = salary_data_frame['year'].apply(str).apply(parse)


    # 社会平均月薪
    data_array = np.array(salary_data_frame[salary_dict['social_average']])
    data_array = data_array / 12
    social_salary_series = pd.Series(data_array, index=salary_date_list.values).sort_index(ascending=True)

    # 国有单位月薪
    data_array = np.array(salary_data_frame[salary_dict['state_owned']])
    data_array = data_array / 12
    print('state_owned_salary_series data_array: ', data_array)
    state_owned_salary_series = pd.Series(data_array, index=salary_date_list.values).sort_index(ascending=True)
    # plt.xticks(salary_data_series.index)
    print('state_owned_salary_series: ', state_owned_salary_series)

    # 房价社会平均收入比
    data_array = house_price.values / social_salary_series.values
    print('house_price.values: ', house_price.values)
    print('social_salary_series.values: ', social_salary_series.values)
    print('data_array', data_array)
    social_ratio_series = pd.Series(data_array, index=salary_date_list.values).sort_index(ascending=True)
    print('social_ratio_series: ', social_ratio_series)
    plt.plot(social_ratio_series.index, social_ratio_series.values, label=xlabel_dict['social_ratio'])
    plt.xticks(social_ratio_series.index)

    # 房价国有单位收入比
    data_array = house_price.values / state_owned_salary_series.values
    state_owned_ratio_series = pd.Series(data_array, index=salary_date_list.values).sort_index(ascending=True)
    plt.plot(state_owned_ratio_series.index, state_owned_ratio_series.values, label=xlabel_dict['state_owned_ratio'])
    plt.xticks(state_owned_ratio_series.index)

    show_ratio_chart(ylabel=ylabel_dict['ration'])

