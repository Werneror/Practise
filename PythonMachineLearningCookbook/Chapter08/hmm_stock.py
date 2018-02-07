# ^_^ coding:utf-8 ^_^

import numpy as np
import matplotlib.pyplot as plt
from hmmlearn.hmm import GaussianHMM

# 从输入文件中加载数据
input_file = 'CNY.csv'
data = np.loadtxt(input_file, delimiter=',')

# 提取需要的值
closing_values = np.array(data[:, 6])
volume_of_shares = np.array(data[:, 8])[:-1]

# 计算每天收盘价变化率
diff_percentage = 100.0 * np.diff(closing_values) / closing_values[:-1]

# 将变化率与交易量组合起来
X = np.column_stack((diff_percentage, volume_of_shares))

# 创建并训练高斯隐马尔科夫模型
print(u"训练高斯隐马尔科夫模型中......")
model = GaussianHMM(n_components=5, covariance_type='diag', n_iter=1000)
model.fit(X)

# 用模型生成数据
num_samples = 500
samples, _ = model.sample(num_samples)
plt.plot(np.arange(num_samples), samples[:, 0], c='black')
plt.figure()
plt.plot(np.arange(num_samples), samples[:, 1], c='red')
plt.show()
