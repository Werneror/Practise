# ^_^ coding:utf-8 ^_^

import numpy as np
import neurolab as nl
import matplotlib.pyplot as plt

# 定义输入数据
input_file = 'data_vq.txt'
input_text = np.loadtxt(input_file)
data = input_text[:, 0:2]
labels = input_text[:, 2:]

# 定义一个两层神经网络，输入含有10个神经元，输出含有4个神经元
# 学习向量量化（Learning Vector Quantization，LVQ）
net = nl.net.newlvq(nl.tool.minmax(data), 10, [0.25, 0.25, 0.25, 0.25])

# 通过100次的迭代训练神经网络
error = net.train(data, labels, epochs=100, goal=-1)

# 创建输入网格
xx, yy = np.meshgrid(np.arange(0, 8, 0.2), np.arange(0, 8, 0.2))
xx.shape = xx.size, 1
yy.shape = yy.size, 1
input_grid = np.concatenate((xx, yy), axis=1)

# 用这些网格点值评价该网络
output_grid = net.sim(input_grid)

# 定义4个类
class1 = data[labels[:, 0] == 1]
class2 = data[labels[:, 1] == 1]
class3 = data[labels[:, 2] == 1]
class4 = data[labels[:, 3] == 1]

# 为4个类定义网格
grid1 = input_grid[output_grid[:, 0] == 1]
grid2 = input_grid[output_grid[:, 1] == 1]
grid3 = input_grid[output_grid[:, 2] == 1]
grid4 = input_grid[output_grid[:, 3] == 1]

# 画出输出结果
plt.plot(class1[:, 0], class1[:, 1], 'ko', class2[:, 0], class2[:, 1], 'ko', class3[:, 0], class3[:, 1], 'ko', class4[:, 0], class4[:, 1], 'ko')
plt.plot(grid1[:, 0], grid1[:, 1], 'b.', grid2[:, 0], grid2[:, 1], 'gx', grid3[:, 0], grid3[:, 1], 'cs', grid4[:, 0], grid4[:, 1], 'ro')
plt.axis([0, 8, 0, 8])
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.title('Vector quantization using neural networks')

plt.show()