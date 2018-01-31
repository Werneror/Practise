# ^-^ coding:utf-8 ^-^

import numpy as np
import matplotlib.pyplot as plt

# 创建一些样本数据
X = np.array([[3, 1], [2 ,5], [1, 8], [6 ,4], [5, 2], [3, 5], [4, 7], [4, -1]])

# 为数据点分配标记
y = [0, 1, 1, 0, 0, 1, 1, 0]

# 按类别标签把数据分为两类
class_0 = np.array([ X[i] for i in range(len(X)) if y[i] ==0 ])
class_1 = np.array([ X[i] for i in range(len(X)) if y[i] ==1 ])

# 画出数据图像
plt.figure()
plt.scatter(class_0[:, 0], class_0[:, 1], color='black', marker='s')
plt.scatter(class_1[:, 0], class_1[:, 1], color='black', marker='x')
plt.show()

# 画一条直线分割数据
line_x = range(10)
line_y = line_x
plt.figure()
plt.scatter(class_0[:, 0], class_0[:, 1], color='black', marker='s')
plt.scatter(class_1[:, 0], class_1[:, 1], color='black', marker='x')
plt.plot(line_x, line_y, color='black', linewidth=3)
plt.show()
plt.show()