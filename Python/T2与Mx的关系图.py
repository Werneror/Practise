#!/usr/lib/python2.7
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt

x = [0,10,20,30,40,50]
y = [14.5914,19.6229,24.6660,29.9092,35.2606,40.5618]
# 设置纵轴的上下限
plt.ylim(0,42)
plt.xlim(0,52)
#添加坐标轴说明
plt.xlabel('Mx(g)')
plt.ylabel('T^2(ms^2)')
#绘制图形
plt.plot(x, y, 'k--o')
plt.show()
