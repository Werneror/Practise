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

# 打印最大值和最小值
print('\n最大值：\n{}'.format(dataframe.max()))
print('\n最小值：\n{}'.format(dataframe.min()))

# 打印均值
print('\n均值：\n{}'.format(dataframe.mean()))
print('\n行均值：\n{}'.format(dataframe.mean(1)[:10]))

# 打印滑动均值
pd.rolling_mean(dataframe, window=24).plot()
plt.title('Correlation coefficients')

# 打印相关系数
print('\n相关系数:\n{}'.format(dataframe.corr()))

# 画出滑动相关性
plt.figure()
pd.rolling_corr(dataframe['first'], dataframe['second'], window=60).plot()
plt.title('rolling corr')

plt.show()