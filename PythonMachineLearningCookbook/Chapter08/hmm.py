# ^_^ coding:utf-8 ^_^

import datetime
import numpy as np 
import matplotlib.pyplot as plt 
from hmmlearn.hmm import GaussianHMM

from convert_to_timeseries import convert_data_to_timeseries

# 从输入文件中加载数据
input_file = 'data_hmm.txt'
data = np.loadtxt(input_file, delimiter=',')

# 排列训练数据
X =np.column_stack([data[:, 2]])

# 创建并训练高斯HMM模型
print(u"训练高斯HMM模型")
num_components = 4
model = GaussianHMM(n_components=num_components,
                                         covariance_type='diag',n_iter=1000)
model.fit(X)

# 预测HMM的隐藏状态
hidden_states = model.predict(X)

# 计算这些隐藏状态的均值和方差
print(u"隐藏状态的均值和方差")
for i in range(model.n_components):
    print(u"隐藏状态：{}".format(i+1))
    print(u"均值：{:.3f}".format(model.means_[i][0]))
    print(u"方差：{:.3f}".format(np.diag(model.covars_[i])[0]))

# 用模型生成数据
num_samples  = 1000
samples, _ = model.sample(num_samples)
plt.plot(np.arange(num_samples), samples[:, 0], c='black')
plt.title('Number of components = {}'.format(num_components))
plt.show()