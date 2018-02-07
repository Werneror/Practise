# ^_^ coding:utf-8 ^_^

import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 

# 定义读取输入文件函数
def convert_data_to_timeseries(input_file, column, verbose=False):

    # 加载输入文件
    data = np.loadtxt(input_file, delimiter=',')

    # 提取起始日期和终止日期
    start_date = str(int(data[0,0])) + '-' + str(int(data[0,1]))
    end_month = int(data[-1,1])
    if end_month == 12:
        end_date = str(int(data[-1,0]+1)) + '-1'
    else:
        end_date = str(int(data[-1,0])) + '-' + str(end_month+1)

    # 打印信息
    if verbose:
        print("\nStart date = {}\nEnd date = {}".format(start_date, end_date))

    # 创建以月为间隔的变量
    dates = pd.date_range(start_date, end_date, freq='M')

    # 打印以月为间隔的变量
    if verbose:
        print("\n{}".format(dates))

    # 将日期转换成时间序列
    data_timeseries = pd.Series(data[:,column], index=dates)

    # 打印出最开始的十个元素
    if verbose:
        print("\nTime series data:\n{}".format(data_timeseries[:10]))

    # 返回时间索引变量
    return data_timeseries

if __name__ == '__main__':

    # 输入数据文件
    input_file = 'data_timeseries.txt'

    # 加载输入数据
    column_num = 2
    data_timeseries = convert_data_to_timeseries(input_file, 
                                                                                  column_num,
                                                                                  True)

    # 画出时序数据
    data_timeseries.plot()
    plt.title('Input data')
    plt.show()