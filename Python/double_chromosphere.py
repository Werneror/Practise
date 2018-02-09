# ^_^ coding:utf-8 ^_^

import json
import numpy as np 
import matplotlib.pyplot as plt 
from hmmlearn.hmm import GaussianHMM

input_file = 'double_chromosphere.json'
with open(input_file, 'r') as f:
    jsons = json.loads(f.read())

datas = []
for json in jsons:
    data = []
    data.append(json['number'])
    data.append(json['red1'])
    data.append(json['red2'])
    data.append(json['red3'])
    data.append(json['red4'])
    data.append(json['red5'])
    data.append(json['red6'])
    data.append(json['blue'])
    datas.append(data)

datas = np.array(datas)
datas = datas[datas[:,0].argsort()]
X =np.column_stack([datas[:, 1:]])

# 创建并训练高斯HMM模型
print(u"训练高斯HMM模型......")
num_components = 4
model = GaussianHMM(n_components=num_components,
                                         covariance_type='diag',n_iter=1000)
model.fit(X)

# 预测HMM的隐藏状态
hidden_states = model.predict(X)

# 预测接下来的一期
num_samples  = 1
samples, _ = model.sample(num_samples)
red = samples[0][:-1].astype(int)
red.sort()
blue = int(samples[0][-1])

# 输出预测结果
print(u"预测结果为：")
print(u"红球：{}，蓝球：{}".format(red, blue))