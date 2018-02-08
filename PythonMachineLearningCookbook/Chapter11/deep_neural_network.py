# ^_^ coding:utf-8 ^_^

import numpy as np
import neurolab as nl
import matplotlib.pyplot as plt

# 生成训练数据
min_value = -12
max_value = 12
num_datapoints = 90

x = np.linspace(min_value, max_value, num_datapoints)
y = 2 * np.square(x) + 7
y /= np.linalg.norm(y)
data = x.reshape(num_datapoints, 1)
labels = y.reshape(num_datapoints, 1)

# 画出输入数据
plt.figure()
plt.scatter(data, labels)
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.title('Input data')

# 定义个神经网络，带两个隐藏层
# 每个隐藏层由10个神经元组成，输出层由一个神经元组成
multilayer_net = nl.net.newff([[min_value, max_value]], [10, 10, 1])

# 设置训练算法为阶梯下降算法
multilayer_net.trainf = nl.train.train_gd

# 训练网络
error = multilayer_net.train(data, labels, epochs=800, show=100, goal=0.01)

predicted_output = multilayer_net.sim(data)

# 画出训练误差结果
plt.figure()
plt.plot(error)
plt.xlabel('Numberr of epochs')
plt.ylabel('Training error')
plt.grid()
plt.title('Training error progress')

# 画出预测结果
x2 = np.linspace(min_value, max_value, num_datapoints * 2)
y2 = multilayer_net.sim(x2.reshape(x2.size, 1)).reshape(x2.size)
y3= predicted_output.reshape(num_datapoints)

plt.figure()
plt.plot(x2, y2, '-', x, y, '.', x, y3, 'p')
plt.title('Ground truth vs predicted output')

plt.show()
plt.show()
