# ^_^ coding:utf-8 ^_^

import numpy as np
import neurolab as nl

# 输入文件
input_file = '/home/werner/Downloads/letter.data'

# 从输入文件中加载数据点
num_datapoints = 20

# 定义不同的字符
orig_labels = 'omandig'

# 不同字符的数量
num_output = len(orig_labels)

# 划分训练集和测试集
num_train = int(0.9 * num_datapoints)
num_test = num_datapoints - num_train

# 定义数据集提取参数
start_index = 6
end_index = -1

# 生成数据集
data = []
labels = []
with open(input_file, 'r') as f:
    for line in f.readlines():
        # 按Tab键分割
        list_vals = line.split('\t')
        # 如果字符不在标签列表中，跳过
        if list_vals[1] not in orig_labels:
            continue
        # 提取标签，并将其添加到主列表的后面
        label = np.zeros((num_output, 1))
        label[orig_labels.index(list_vals[1])] = 1
        labels.append(label)
        # 提取字符，并将其添加到主列表的后面
        cur_char = np.array([float(x) for x in list_vals[start_index: end_index]])
        data.append(cur_char)
        # 当有足够多数据时跳出循环
        if len(data) >= num_datapoints:
            break

# 将数据转换为Numpy数组
data = np.asfarray(data)
labels = np.array(labels).reshape(num_datapoints, num_output)

# 提取数据的维度信息
num_dims = len(data[0])

# 创建并训练神经网络
net = nl.net.newff([[0, 1] for _ in range(len(data[0]))], [128, 16, num_output])
net.trainf = nl.train.train_gd
error = net.train(data[:num_train, :], labels[:num_train, :], epochs=1000, show=100, goal=0.01)

# 为测试输入数据预测输出结构
predicted_output = net.sim(data[num_train:, :])
print(u"用未知数据做测试：")
for i in range(num_test):
    print(u"输入：{}".format(orig_labels[np.argmax(labels[i])]))
    print(u"预测：{}".format(orig_labels[np.argmax(predicted_output[i])]))