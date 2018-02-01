#coding:utf-8

import csv
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 载入字体
myfont = fm.FontProperties(fname='/usr/share/fonts/mine/汉仪小隶书简.ttf')

# 载入数据
file_name = "mbti_distribution.csv"
with open(file_name) as f:
	reader = csv.reader(f)
	mbti = list(reader)[1:]

types = [x[0] for x in mbti]
describe = [x[1] for x in mbti]
population =  [float(x[2]) for x in mbti]
male =  [float(x[3]) for x in mbti]
female =  [float(x[4]) for x in mbti]
x = list(range(0,16))

# 绘制分布柱状图

plt.clf()
plt.suptitle("MBTI性格分布图",fontproperties=myfont, fontsize=25)

plt.subplot(211)
plt.xlabel("MBTI性格类型",fontproperties=myfont, fontsize=20)
plt.ylabel("总人口中比例(%)",fontproperties=myfont, fontsize=20)
plt.ylim(0, 15)
plt.bar(x=x, height=population)
plt.xticks(x, types)
for x_,y in zip(x,population):  
	plt.text(x_, y+0.7, '%.2f' % y, ha='center', va='top')

plt.subplot(223)
plt.xlabel("MBTI性格类型",fontproperties=myfont, fontsize=20)
plt.ylabel("男性中比例(%)",fontproperties=myfont, fontsize=20)
plt.ylim(0, 17)
plt.bar(x=x, height=male)
plt.xticks(x, types)
for x_,y in zip(x,male):  
	plt.text(x_, y+0.8, '%.2f' % y, ha='center', va='top')

plt.subplot(224)
plt.xlabel("MBTI性格类型",fontproperties=myfont, fontsize=20)
plt.ylabel("女性中比例(%)",fontproperties=myfont, fontsize=20)
plt.ylim(0, 17)
plt.bar(x=x, height=female)
plt.xticks(x, types)
for x_,y in zip(x,female):
	plt.text(x_, y+0.8, '%.2f' % y, ha='center', va='top')

plt.show()