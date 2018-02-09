# ^_^ coding:utf-8 ^_^

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.mlab import csv2rec
import matplotlib.cbook as cbook
from matplotlib.ticker import Formatter

# 定义一个类将日期格式化
class DataFormatter(Formatter):
    def __init__(self, dates, date_format='%Y-%m-%d'):
        self.dates = dates
        self.date_format = date_format

    def __call__(self, t, position=0):
        index = int(round(t))
        if index >= len(self.dates) or index < 0:
            return ''
        return self.dates[index].strftime(self.date_format)

if __name__ == '__main__':
    #输入包含股价的CSV文件
    input_file = cbook.get_sample_data('apple.csv', asfileobj=False)

    # 将CSV文件加载到numpy记录数组中
    data = csv2rec(input_file)

    # 提取子集
    data = data[-70:]

    # 创建一个日期格式化对象
    formatter = DataFormatter(data.date)

    # X轴为时间
    x_vals = numpy.arange(len(data))

    # Y轴为收盘价
    y_vals = data.close

    # 画出数据
    fig, ax = plt.subplots()
    ax.xaxis.set_major_formatter(formatter)
    ax.plot(x_vals, y_vals, 'o-')
    fig.autofmt_xdate()
    plt.show()
