# ^_^ coding:utf-8 ^_^

import numpy as np 
from sklearn import preprocessing
from sklearn import cross_validation
from sklearn.svm import SVC

input_file = 'building_event_binary.txt'

# 读取数据
X = []
count = 0
with open(input_file, 'r') as f:
	for line in f.readlines():
		data = line[:-1].split(',')
		X.append([data[0]]+data[2:]) #这里略去了日期
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

# 用径向基函数、概率输出和类型平均方法训练SVM分类器
params = {'kernel':'rbf', 'probability':True}
classifier = SVC(**params)
classifier.fit(X, y)

# 进行交叉验证
accuracy = cross_validation.cross_val_score(classifier, X, y, scoring='accuracy', cv=5)
print(u"分类器准确度为：{:.2f}%".format(accuracy.mean()*100))

# 对单一数据示例进行编码测试
input_data = ['Tuesday', '12:30:00', '21', '23']
input_data_encoded = [-1]*len(input_data)
count = 0
for i,item in enumerate(input_data):
	if item.isdigit():
		input_data_encoded[i] = int(input_data[i])
	else:
		input_data_encoded[i] = int(label_encoder[count].transform([input_data[i]]))
		count += 1
input_data_encoded = np.array(input_data_encoded)

output_class = classifier.predict([input_data_encoded])
print(u"预测类：{}".format(label_encoder[-1].inverse_transform(output_class)[0]))