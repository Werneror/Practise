# ^_^ coding:utf-8 ^_^

import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 

from convert_to_timeseries import convert_data_to_timeseries

# 输入数据文件
input_file = 'data_timeseries.txt'

# 加载输入数据
column_num = 2
data_timeseries = convert_data_to_timeseries(input_file, column_num)

# 确定画图起止年份
start = '2008'
end = '2015'

# 画出给定年份范围内数据
plt.figure()
data_timeseries[start:end].plot()
plt.title('Data from {} to {}'.format(start, end))
plt.show()

# 确定画图起止年月
start = '2007-2'
end = '2017-11'

# 画出给定年月范围内数据
plt.figure()
data_timeseries[start:end].plot()
plt.title('Data from {} to {}'.format(start, end))
plt.show()