#!/usr/bin/env python3
# coding: utf-8

import numpy as np
import pandas as pd
from visdom import Visdom
import matplotlib.pyplot as plt
import seaborn
seaborn.set()
import os, time, sys, pickle


if __name__=='__main__':
    if len(sys.argv) < 2:
        print("pls enter dataset file path!")
        raise SystemExit(1)

    csv_data_file = sys.argv[1]
    data_frame = pd.read_csv(csv_data_file)
    date_list = np.array(data_frame['date'])
    name = data_frame['industry_name'][0]
    history_count = np.array(data_frame['company_count'])
    static_pe_average = np.array(data_frame['static_pe_average'])
    static_pe_median = np.array(data_frame['static_pe_median'])
    dynamic_pe_average = np.array(data_frame['dynamic_pe_average'])
    dynamic_pe_median = np.array(data_frame['dynamic_pe_median'])
    print(name)
    print(data_frame.index)
    print(data_frame.columns)
    dpa_data_series = pd.Series(dynamic_pe_average, index=date_list).sort_index(ascending=False)
    print(dpa_data_series)
   # plt.hist(dpa_data_series)
   # plt.title('industry history pe')
   # plt.xlabel('date')
   # plt.ylabel('pe')

    viz = Visdom(env='main')
    viz.matplot(dpa_data_series.plot())


