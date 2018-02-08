# ^_^ coding:utf-8 ^_^

import numpy as np
import neurolab as nl
import matplotlib.pyplot as plt

# 定义输入数据
input_file = 'data_single_layer.txt'
input_text = np.loadtxt(input_file)
data = input_text[:, 0:2]
labels = input_text[:, 2:]

# 画出输入数据
plt.figure()
plt.scatter(data[:, 0], data[:, 1])
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.title('Input data')

# 提取每个维度的最小值和最大值
x_min, x_max = data[:, 0].min(), data[:, 0].max()
y_min, y_max = data[:, 1].min(), data[:, 1].max()

# 定义一个单层神经网络，包含两个神经元
# 在感知器第一个参数的每个元素中指定参数的最大和最小值
single_layer_net = nl.net.newp([[x_min, x_max], [y_min, y_max]], 2)

# 通过50次的迭代训练神经网络
error = single_layer_net.train(data, labels, epochs=50, show=20, lr=0.01)

# 画出结果
plt.figure()
plt.plot(error)
plt.xlabel('Numberr of epochs')
plt.ylabel('Training error')
plt.grid()
plt.title('Training error progress')

plt.show()

# 用新的数据测试神经网络
print(single_layer_net.sim([[0.3, 4.5]]))
print(single_layer_net.sim([[4.5, 0.5]]))
print(single_layer_net.sim([[4.3, 8]]))
