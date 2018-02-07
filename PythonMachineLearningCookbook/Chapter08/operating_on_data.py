# ^_^ coding:utf-8 ^_^

import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 

from convert_to_timeseries import convert_data_to_timeseries

# 输入数据文件
input_file = 'data_timeseries.txt'

# 加载输入数据
data1 = convert_data_to_timeseries(input_file, 2)
data2 = convert_data_to_timeseries(input_file, 3)

# 将数据转换为pandas的数据帧
dataframe = pd.DataFrame({'first': data1, 'second': data2})

# 画图
dataframe['1952':'1955'].plot()
plt.title('Data overlapped on top of each other')

# 画出两组数据的不同
plt.figure()
difference = dataframe['1952':'1955']['first'] - dataframe['1952':'1955']['second']
difference.plot()
plt.title('Difference (first - second)')

# 当“first”大于某个阈值且“second”小于某个阈值时
dataframe[(dataframe['first']>60) & (dataframe['second']<20)].plot()
plt.title('first > 60 and second < 20')
plt.show()