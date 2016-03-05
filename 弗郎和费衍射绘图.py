#!/usr/bin/env python
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt

#只用改下面两个变量
naturallight = 0.046	#这个变量的值是自然光强对应的电流值
data =[0.122,0.107,0.099,0.105,0.125,0.164,0.217,0.293,0.373,0.456,0.543,0.616,0.675,0.710,0.713,0.684,0.620,0.527,0.421,0.316,0.207,0.143,0.142,0.228,0.425,0.741,1.216,1.892,2.70,3.62,4.77,6.05,7.41,8.88,10.25,11.62,12.88,14.03,14.99,15.61,16.03,16.13,15.95,15.47,14.70,13.70,12.53,11.18,9.75,8.36,6.87,5.50,4.28,3.15,2.26,1.52,0.961,0.553,0.305,0.190,0.174,0.231,0.329,0.457,0.573,0.673,0.735,0.765,0.754,0.712,0.640,0.554,0.458,0.356,0.265,0.189,0.133,0.100,0.091,0.100]

x = []
y = []
leng = 0.3		#测量间距为0.3毫米
maxdata = max(data)	#获取列表中的最大元素
a = data.index(maxdata)	#获取最大元素的下脚标
#生成散点的x坐标值
for i in range(-a,len(data)-a):
	x.append(i*leng)
#生成散点的y坐标值
for i in data:
	y.append((i-naturallight+0.008)/maxdata)
# 设置纵轴的上下限
plt.ylim(0,1.1)
#将坐标轴调整到中央
ax = plt.gca()
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.xaxis.set_ticks_position('bottom')
ax.spines['bottom'].set_position(('data',0))
ax.yaxis.set_ticks_position('left')
ax.spines['left'].set_position(('data',0))
#添加坐标轴说明
plt.title('I/I.')	#以此代替y轴说明
plt.xlabel('x(mm)')
plt.xticks(x[::2])
#绘制图形
plt.plot(x, y, 'k--o')
plt.show()
