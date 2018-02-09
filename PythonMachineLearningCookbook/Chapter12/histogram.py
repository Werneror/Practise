# ^_^ coding:utf-8 ^_^

import numpy as np
import matplotlib.pyplot as plt

# 输入数据
apples = [30, 25, 22, 36, 21, 29]
oranges = [24, 33, 19, 27, 35, 20]

# 设置数组
num_groups = len(apples)

# 创建图象
fig, ax = plt.subplots()

# 定义X轴
indices = np.arange(num_groups)

# 直方图的宽度和透明度
bar_width = 0.4
opacity = 0.6

# 画直方图
hist_apples = plt.bar(indices, apples, bar_width, alpha=opacity, color='g', label='Apples')
hist_oranges = plt.bar(indices+bar_width, oranges, bar_width, alpha=opacity, color='b', label='Oranges')

# 设置直方图参数
plt.xlabel('Month')
plt.ylabel('Production quantity')
plt.title('Comparing apples and oranges')
plt.xticks(indices + bar_width, ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'))
plt.ylim([0, 45])
plt.legend()
plt.tight_layout()

plt.show()