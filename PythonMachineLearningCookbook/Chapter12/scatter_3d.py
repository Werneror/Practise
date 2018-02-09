# ^_^ coding:utf-8 ^_^

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# 生成一个空白图象
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# 定义生成的值的个数
n = 250

# 生成lambda函数来生成给定范围的值
f = lambda minval, maxval, n: minval + (maxval - minval) * np.random.rand(n)

# 生成X, Y 和Z的值
x_vals = f(15, 41, n)
y_vals = f(-10, 70, n)
z_vals = f(-52, -37, n)

# 画出这些值
ax.scatter(x_vals, y_vals, z_vals, c='k', marker='o')
ax.set_xlabel('X axis')
ax.set_ylabel('Y axis')
ax.set_zlabel('Z axis')

plt.show()