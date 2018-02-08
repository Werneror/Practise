# ^_^ coding:utf-8 ^_^

import numpy as np
import neurolab as nl
import matplotlib.pyplot as plt

# 定义输入数据
data = np.array([[0.3, 0.2], [0.1, 0.4], [0.4, 0.6], [0.9, 0.5]])
labels = np.array([[0], [0], [0], [1]])

# 画出输入数据
plt.figure()
plt.scatter(data[:, 0], data[:, 1])
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.title('Input data')

# 定义有两个输入的感知器
# 在感知器第一个参数的每个元素中指定参数的最大和最小值
perceptron = nl.net.newp([[0, 1], [0, 1]], 1)

# 训练感知器
error = perceptron.train(data, labels, epochs=50, show=15, lr=0.01)

# 画出结果
plt.figure()
plt.plot(error)
plt.xlabel('Numberr of epochs')
plt.ylabel('Training error')
plt.grid()
plt.title('Training error progress')

plt.show()
