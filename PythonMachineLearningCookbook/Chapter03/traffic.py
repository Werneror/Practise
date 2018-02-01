# ^_^ coding:utf-8 ^_^

import numpy as np 
from sklearn import preprocessing
from sklearn.svm import SVR
import sklearn.metrics as sm

input_file = 'traffic_data.txt'

# 读取数据
X =[]
count = 0
with open(input_file, 'r') as f:
	for line in f.readlines():
		data = line[:-1].split(',')
		X.append(data)
X = np.array(X)

# 将字符串转换成数值数据
label_encoder = []
X_encoded = np.empty(X.shape)
for i, item in enumerate(X[0]):
	if item.isdigit():
		X_encoded[:, i] = X[:, i]
	else:
		label_encoder.append(preprocessing.LabelEncoder())
		X_encoded[:, i] = label_encoder[-1].fit_transform(X[:, i])
X = X_encoded[:, :-1].astype(int)
y = X_encoded[:, -1].astype(int)

# 用径向基函数创建并训练SVM分类器
params = {'kernel': 'rbf', 'C': 10.0, 'epsilon': 0.2}
regressor = SVR(**params)
regressor.fit(X, y)

# 用交叉验证来检查回归器的性能
y_pred = regressor.predict(X)
print(u"平均绝对误差：{:.2f}".format(sm.mean_absolute_error(y, y_pred)))

# 对单一数据示例进行编码测试
input_data = ['Tuesday', '13:35', 'San Francisco', 'yes']
input_data_encoded = [-1]*len(input_data)
count = 0
for i,item in enumerate(input_data):
	if item.isdigit():
		input_data_encoded[i] = int(input_data[i])
	else:
		input_data_encoded[i] = int(label_encoder[count].transform([input_data[i]]))
		count += 1
input_data_encoded = np.array(input_data_encoded)

print(u"输出值：{}".format(regressor.predict([input_data_encoded])[0]))