# ^_^ coding:utf:8 ^_^

import numpy as np
from sklearn import preprocessing
from sklearn import cross_validation
from sklearn.naive_bayes import GaussianNB

# 加载数据集
input_file = 'adult.data.txt'

# 读取数据
X = []
y = []
count_lessthan50k = 0
count_morethan50k = 0
num_images_threshold = 10000

# 读入每种类型10000个数据
with open(input_file, 'r') as f:
	for line in f.readlines():
		if '?' in line:
			continue
		data = line[:-1].split(', ')
		if data[-1] == '<=50K' and count_lessthan50k < num_images_threshold:
			X.append(data)
			count_lessthan50k = count_lessthan50k + 1
		if data[-1] == '>50K' and count_morethan50k < num_images_threshold:
			X.append(data)
			count_morethan50k = count_morethan50k + 1
		if count_lessthan50k >= num_images_threshold and count_morethan50k >= num_images_threshold:
			break

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


# 交叉验证
X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.25, random_state=5)

# 建立分类器
classifier_gaussiannb = GaussianNB()
classifier_gaussiannb.fit(X_train, y_train)
y_test_pred = classifier_gaussiannb.predict(X_test)

# 计算分类器的F1得分
f1 = cross_validation.cross_val_score(classifier_gaussiannb,
	X, y, scoring='f1_weighted', cv=5)
print(u"F1得分为：{0:.2f}%".format(100*f1.mean()))

# 对单一数据示例进行编码测试
input_data = ['39','State-gov','77516','Bachelors','13','Never-married','Adm-clerical','Not-in-family','White','Male','2174','0','40','United-States']
count = 0
input_data_encoder = [-1]*len(input_data)
for i,item in enumerate(input_data):
	if item.isdigit():
		input_data_encoder[i] = int(input_data[i])
	else:
		input_data_encoder[i] = int(label_encoder[count].transform([input_data[i]]))
		count = count + 1
input_data_encoder = np.array(input_data_encoder)

# 预测并打印特定数据点的输出结果
output_class = classifier_gaussiannb.predict([input_data_encoder])
print(label_encoder[-1].inverse_transform(output_class))[0]