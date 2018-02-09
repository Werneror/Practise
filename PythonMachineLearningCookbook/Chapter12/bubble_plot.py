# ^_^ coding:utf-8 ^_^

import numpy as np
import matplotlib.pyplot as plt

# 定义值的个数
num_vals = 400

# 生成随机数
x = np.random.rand(num_vals)
y = np.random.rand(num_vals)

# 定义每个点的面积
# 指定最大半径
max_radius = 25
area = np.pi * (max_radius * np.random.rand(num_vals)) ** 2

# 生成颜色
colors = np.random.rand(num_vals)

# 画出数据点
plt.scatter(x, y, s=area, c=colors, alpha=0.6)

plt.show()