# ^-^ coding:utf-8 ^-^
from sklearn import preprocessing

# 定义标记编码器（laber encoder）
label_encoder = preprocessing.LabelEncoder()

# 创建标记
input_class = ['audi', 'ford', 'audi', 'toyota', 'ford', 'bmw']
label_encoder.fit(input_class)
print(u"标记映射：")
for i, item in enumerate(label_encoder.classes_):
	print item, '-->', i
print("\n")

# 使用标记映射
labels = ['toyota', 'ford', 'audi']
encoded_labels = label_encoder.transform(labels)
print(u"标记 = {}".format(labels))
print(u"编码 = {}".format(list(encoded_labels)))
print("\n")

# 编码返向转回标记
encoded_labels = [2, 1, 0, 3, 1]
decoded_labels = label_encoder.inverse_transform(encoded_labels)
print(u"编码：{}".format(encoded_labels))
print(u"解码：{}".format(decoded_labels))