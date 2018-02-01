# ^_^ coding:utf-8 ^_^

import numpy as np 
import matplotlib.pyplot as plt 

def plot_classifier(classifier, X ,y, title='Classifier boundaries', annotate=False):
	# 定义图形的取值范围
	x_min, x_max = min(X[:, 0]) - 1.0, max(X[:, 0]) + 1.0
	y_min, y_max = min(X[:, 1]) - 1.0, max(X[:, 1]) + 1.0

	# 设置网格数据步长
	step_size = 0.01

	# 定义网格
	x_values, y_values = np.meshgrid(np.arange(x_min, x_max, step_size), np.arange(y_min, y_max, step_size))

	# 计算分类器输出结果
	mesh_output = classifier.predict(np.c_[x_values.ravel(), y_values.ravel()])

	# 数组维度变形
	mesh_output  = mesh_output.reshape(x_values.shape)

	plt.figure()

	# 设置标题
	plt.title(title)

	# 用彩色画出分类结果
	plt.pcolormesh(x_values, y_values, mesh_output, cmap=plt.cm.gray)

	# 将训练点画在图上
	plt.scatter(X[:, 0], X[:, 1], c=y, s=80, edgecolors='black', linewidth=1, cmap=plt.cm.Paired)

	# 设置图形的取值范围
	plt.xlim(x_values.min(), x_values.max())
	plt.ylim(y_values.min(), y_values.max())

	# 设置X轴和Y轴
	plt.xticks(())
	plt.yticks(())


	if annotate:
		for x, y in zip(X[:, 0], X[:, 1]):
		# Full documentation of the function available here: 
		# http://matplotlib.org/api/text_api.html#matplotlib.text.Annotation
			plt.annotate(
				'(' + str(round(x, 1)) + ',' + str(round(y, 1)) + ')',
				xy = (x, y), xytext = (-15, 15), 
				textcoords = 'offset points', 
				horizontalalignment = 'right', 
				verticalalignment = 'bottom', 
				bbox = dict(boxstyle = 'round,pad=0.6', fc = 'white', alpha = 0.8),
				arrowprops = dict(arrowstyle = '-', connectionstyle = 'arc3,rad=0'))
	


def load_data(input_file):
	X = []
	y = []
	with open(input_file, 'r') as f:
		for line in f.readlines():
			data = [ float(x) for x in line.split(',') ]
			X.append(data[:-1])
			y.append(data[-1])
	X = np.array(X)
	y = np.array(y)

	return X, y
