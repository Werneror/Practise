# ^_^ coding:utf-8 ^_^

import os
import sys

import cv2
import numpy as np

# 加载数据
input_file = '/home/werner/Downloads/letter.data'

# 定义可视化参数
scaling_factor = 10
start_index = 6
end_index = -1
h, w = 16, 8

# 循环直到用户按下Esc键
with open(input_file, 'r') as f:
    for line in f.readlines():
        data = np.array([255 * float(x) for x in line.split('\t')[start_index: end_index]])

        img = np.reshape(data, (h, w))
        img_scaled = cv2.resize(img, None, fx=scaling_factor, fy=scaling_factor)
        cv2.imshow('Image', img_scaled)

        c = cv2.waitKey()
        if c == 27:
            break
