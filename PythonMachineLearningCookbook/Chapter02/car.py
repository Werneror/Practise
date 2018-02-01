# ^-^ coding:utf-8 ^-^

import numpy as np
import matplotlib.pyplot as plt
from sklearn import preprocessing
from sklearn import cross_validation
from sklearn.learning_curve import learning_curve
from sklearn.learning_curve import validation_curve
from sklearn.ensemble import RandomForestClassifier

# 加载数据集
input_file = 'car.data.txt'

# 读取数据
X = []
count = 0
with open(input_file, 'r') as f:
	for line in f.readlines():
		data = line[:-1].split(',')
		X.append(data)

X = np.array(X)

# 将字符串转换为数字
label_encoder = []
X_encoded = np.empty(X.shape)
for i,item in enumerate(X[0]):
	label_encoder.append(preprocessing.LabelEncoder())
	X_encoded[:, i]= label_encoder[-1].fit_transform(X[:,i])

X = X_encoded[ : , :-1].astype(int)
y = X_encoded[ : ,  -1].astype(int)

# 建立随即森林分类器
params = {'n_estimators':200, 'max_depth':8, 'random_state':7}
classifier = RandomForestClassifier(**params)
classifier.fit(X, y)

# 交叉验证
accuracy = cross_validation.cross_val_score(classifier, X, y, scoring='accuracy', cv=3)
print(u"分类器精度为：{0:.2f}%".format(100*accuracy.mean()))

# 对单一数据示例进行编码测试
input_data = ['vhigh', 'vhigh', '2', '2', 'small', 'low']
input_data_encoded = [-1]*len(input_data)
for i,item in enumerate(input_data):
	input_data_encoded[i] = int(label_encoder[i].transform([input_data[i]]))

input_data_encoded = [np.array(input_data_encoded)]

# 预测并打印特定点的输出
output_class = classifier.predict(input_data_encoded)
print(u"输入为：{}时预测为：{}".format(input_data, label_encoder[-1].inverse_transform(output_class)[0]))


#### 2.10 生成验证曲线 ####

# 参数n_estimators对训练结果的影响
classifier = RandomForestClassifier(max_depth=4, random_state=7)
params_grid = np.linspace(25, 200, 8).astype(int)
train_scores, validation_scores = validation_curve(classifier, X,  y, 'n_estimators', params_grid, cv=5)
print(u"参数n_estimators对训练结果的影响")
print(u"参数：n_estimators，训练得分：")
print(train_scores)
print(u"参数：n_estimators，验证得分：")
print(validation_scores)

# 画出曲线图
plt.figure()
plt.plot(params_grid, 100*np.average(train_scores, axis=1,), color='black')
plt.title('Training curve')
plt.xlabel('Number of estimators')
plt.ylabel('Accuracy')
plt.show()


# 参数max_depth对训练结果的影响
classifier = RandomForestClassifier(n_estimators=20, random_state=7)
params_grid = np.linspace(2, 10, 5).astype(int)
train_scores, validation_scores = validation_curve(classifier, X,  y, 'max_depth', params_grid, cv=5)
print(u"参数max_depth对训练结果的影响")
print(u"参数：max_depth，训练得分：")
print(train_scores)
print(u"参数：max_depth，验证得分：")
print(validation_scores)

# 画出曲线图
plt.figure()
plt.plot(params_grid, 100*np.average(train_scores, axis=1,), color='black')
plt.title('Training curve')
plt.xlabel('Maximum depth of the tree')
plt.ylabel('Accuracy')
plt.show()


#### 2.11 生成学习曲线 ####

classifier = RandomForestClassifier(random_state=7)
params_grid = np.array([200, 500, 800, 1100])
train_sizes, train_scores, validation_scores = learning_curve(classifier,
	X, y, train_sizes=params_grid, cv=5)
print(u"学习曲线")
print(u"训练得分：\n{}".format(train_scores))
print(u"测试得分：\n{}".format(validation_scores))

# 画出曲线图
plt.figure()
plt.plot(params_grid, 100*np.average(train_scores, axis=1,), color='black')
plt.title('Learning curve')
plt.xlabel('Number of training samples')
plt.ylabel('Accuracy')
plt.show()