# ^_^ coding:utf-8 ^_^

import argparse

import numpy as np 
from scipy import misc
from sklearn import cluster
import matplotlib.pyplot as plt 

# 解析输入参数
def build_arg_parser():
	parser = argparse.ArgumentParser(description='Compress the input image using clustering')
	parser.add_argument("--input-file", dest="input_file", required=True, help="Input image")
	parser.add_argument("--num-bits", dest="num_bits", required=True, type=int, help="Number of bits used to represent each pixel")
	return parser

# 压缩输入图片
def compress_image(img, num_clusters):
	# 将输入的图片转换成（样本量，特征量）数组，以运行k-means聚类算法
	X = img.reshape((-1, 1))

	# 对输入数据运行k-means聚类
	kmeans = cluster.KMeans(n_clusters=num_clusters, n_init=4, random_state=5)
	kmeans.fit(X)
	centroids= kmeans.cluster_centers_.squeeze()
	labels = kmeans.labels_
	print(labels)
	# 为每个数据配置离它最近的中心点，并转变为图片的形状
	input_image_compressed = np.choose(labels, centroids).reshape(img.shape)

	return input_image_compressed

# 定义画图函数
def plot_image(img, title):
	vmin = img.min()
	vmax = img.max()
	plt.figure()
	plt.title(title)
	plt.imshow(img, cmap=plt.cm.gray,vmin=vmin, vmax=vmax)

if __name__ == '__main__':
	args = build_arg_parser().parse_args()
	input_file = args.input_file
	num_bits = args.num_bits

	if not 1<= num_bits <= 4:
		raise TypeError('Number of bits should be between 1 and 4')
	num_clusters = np.power(2, num_bits)

	# 打印压缩率
	compression_rate = round(100*(8.0-args.num_bits)/8.0, 2)
	print(u"图片压缩因子为：{}".format(8.0/args.num_bits))
	print(u"图片压缩率为：{}%".format(compression_rate))

	# 加载输入图片
	input_image = misc.imread(input_file, True).astype(np.uint8)

	# 显示原始图片
	plot_image(input_image, 'Original image')

	# 压缩图片
	input_image_compressed = compress_image(input_image, num_clusters)

	# 显示压缩后图片
	plot_image(input_image_compressed, 'Compressed image; compression rate = {}%'.format(compression_rate))
	plt.show()