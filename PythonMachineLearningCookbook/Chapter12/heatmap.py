# ^_^ coding:utf-8 ^_^

import numpy as np
import matplotlib.pyplot as plt

# 定义两组数据
group1 = ['France', 'Italy', 'Spain', 'Portugal', 'Germany']
group2 = ['China', 'Japan', 'Brzail', 'Russia', 'Australia']

# 生成一些随机数
data = np.random.rand(5, 5)

# 创建一个图象
fig, ax = plt.subplots()

# 创建一个热力图
heatmap = ax.pcolor(data, cmap=plt.cm.gray)

# 将坐标轴方在图块的中央
ax.set_xticks(np.arange(data.shape[0]) + 0.5, minor=False)
ax.set_yticks(np.arange(data.shape[1]) + 0.5, minor=False)

# 让热力图显示成一张表
ax.invert_yaxis()
ax.xaxis.tick_top()

# 增加坐标轴标签
ax.set_xticklabels(group2, minor=False)
ax.set_yticklabels(group1, minor=False)

plt.show()