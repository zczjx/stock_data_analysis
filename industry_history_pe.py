#!/usr/bin/env python3
# coding: utf-8

from industry_pe_common import *

if __name__=='__main__':
    if len(sys.argv) < 2:
        print("please enter Industry code index file path")
        raise SystemExit(1)
    global default_dateset_path
    industry_code_file_f = open(sys.argv[1], 'r+', encoding='utf-8-sig')
    industry_code_dict= json.load(industry_code_file_f)
    industry_code_file_f.close()
    # print(industry_code_dict)
    for item in industry_code_dict:
        print(item, ': ', industry_code_dict[item])
    print('请从以上代码中选择要显示的行业代码列表, 用空格键分隔, 忽略大小写: ')
    input_code_list = input().upper().split(' ')
    print(input_code_list)
    print(default_dateset_path)
    for item in titles:
        print(item, ': ', titles[item])
    print('请以上选项中选择您要显示的PE类型 ')
    pe_key = input()
    max_pe = 0.0
    for code in input_code_list:
        csv_data_file = default_dateset_path + code + '.csv'
        data_frame = pd.read_csv(csv_data_file)
        date_list = data_frame['date'].apply(str).apply(parse)
        name = data_frame['industry_name'][0]
        industry_code = data_frame['industry_code'][0]
        history_count = np.array(data_frame['company_count'])
        pe_data_array = np.array(data_frame[pe_options[pe_key]])
        print(name)
        print(data_frame.index)
        print(data_frame.columns)
        dpa_data_series = pd.Series(pe_data_array, index=date_list.values).sort_index(ascending=False)
        dpa_data_series = filter_exception_date_in_series(data_series=dpa_data_series)
        tmp_max_val = dpa_data_series.values.max()
        print('tmp_max_val: ', tmp_max_val)
        if max_pe < tmp_max_val:
            max_pe = tmp_max_val
        print(dpa_data_series)
        plt.plot(dpa_data_series.index, dpa_data_series.values, label=industry_code + name)
    show_pe_chart(max_pe=max_pe, pe_key=pe_key)
