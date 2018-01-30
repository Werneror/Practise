# ^-^ coding:utf-8 ^-^
import numpy as np
from sklearn import preprocessing

# 准备工作
data = np.array([[3, -1.5, 2, -5.4], [0, 4, -0.3, 2.1], [1, 3.3, -1.9, -4.3]])
print(u"原始数据 =\n{}\n".format(data))

# 均值移除（Mean removal），消除偏差（bias）
data_standardized = preprocessing.scale(data)
print(u"均值移除后的数据 =\n{}".format(data_standardized))
print(u"均值移除后的均值 = {}".format(data_standardized.mean(axis=0)))
print(u"均值移除后标准差 = {}\n".format(data_standardized.std(axis=0)))

# 范围缩放（Scaling），将特征的数值范围缩放到合理大小
data_scaler = preprocessing.MinMaxScaler(feature_range=(0,1))
data_scaled = data_scaler.fit_transform(data)
print(u"范围缩放后数据 =\n{}\n".format(data_scaled))

# 归一化（Normalization），常用的归一化形式是将特征向量调整为L1范数（特征向量的数值之和为1）
data_normalized = preprocessing.normalize(data, norm='l1')
print(u"L1归一化数据 =\n{}\n".format(data_normalized))

# 二值化（Binarization），将数据特征向量转换为布尔类型向量
data_binarized = preprocessing.Binarizer(threshold=1.4).transform(data)
print(u"二值化数据 =\n{}\n".format(data_binarized))

# 独热编码，收紧特征向量，one-of-k编码
data = [[0, 2, 1, 12], [1, 3, 5, 3], [2, 3, 2, 12], [1 ,2 ,4 ,3]]
print(u"独热编码前数据 = {}".format(data))
print(u"待编码数据 = {}".format([[2, 3, 5, 3]]))
encoder = preprocessing.OneHotEncoder()
encoder.fit(data)
encoder_vector = encoder.transform([[2, 3, 5, 3]]).toarray()
print(u"独热编码后数据 = {}".format(encoder_vector))