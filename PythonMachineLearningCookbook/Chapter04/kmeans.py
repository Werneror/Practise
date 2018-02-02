# ^_^ coding:utf-8 ^_^

import numpy as np
from sklearn import metrics
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

import utilities

# 加载数据
data = utilities.load_data('data_multivar.txt')
num_vlusters = 4

# 绘制数据
plt.figure()
plt.scatter(data[:,0], data[:,1], marker='o', facecolors='none', edgecolors='k', s=30)
x_min, x_max = min(data[:,0]) -1, max(data[:,0])+1
y_min, y_max = min(data[:,1]) -1, max(data[:,1])+1
plt.title('Input data')
plt.xlim(x_min, x_max)
plt.ylim(y_min, y_max)
plt.xticks(())
plt.yticks(())
plt.show()

# 训练模型
kmeans = KMeans(init='k-means++', n_clusters=num_vlusters, n_init=10)
kmeans.fit(data)

# 可视化边界
step_size = 0.01
x_values, y_values = np.meshgrid(np.arange(x_min, x_max, step_size), np.arange(y_min, y_max, step_size))
predicted_labels = kmeans.predict(np.c_[x_values.ravel(), y_values.ravel()])

# 画出聚类结果
predicted_labels = predicted_labels.reshape(x_values.shape)
plt.figure()
plt.clf()
plt.imshow(predicted_labels,
	      interpolation='nearest', 
	      extent=(x_values.min(), x_values.max(), y_values.min(), y_values.max()),
	      cmap=plt.cm.Paired,
	      aspect='auto',
	      origin='lower')
plt.scatter(data[:,0], data[:,1], marker='o', facecolors='none', edgecolors='k', s=30)

# 把中心点画在图出
centroids = kmeans.cluster_centers_
plt.scatter(centroids[:,0], centroids[:,1], marker='o', s=200, linewidths=3, color='k', zorder=10, facecolors='black')
plt.title('Centoids and boundaries obtained using KMeans')
plt.xlim(x_min, x_max)
plt.ylim(y_min, y_max)
plt.xticks(())
plt.yticks(())
plt.show()