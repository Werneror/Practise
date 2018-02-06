# ^_^ coding:utf-8 ^_^

import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt
from python_speech_features import mfcc, logfbank

# 读取输入的音频文件
sampling_freq, audio = wavfile.read('input_freq.wav')

# 提取MFCC和过滤器组特征
mfcc_features = mfcc(audio, sampling_freq)
filterbank_features = logfbank(audio, sampling_freq)

# 打印参数
print('MFCCL Number of windows = {}'.format(mfcc_features.shape[0]))
print('Length of each feature = {}'.format(mfcc_features.shape[1]))
print('Filter bank: Number of windows = {}'.format(filterbank_features.shape[0]))
print('Length of each feature = {}'.format(filterbank_features.shape[1]))

# 画出特征图
mfcc_features = mfcc_features.T
plt.matshow(mfcc_features)
plt.title('MFCC')

# 将滤波器组特征可视化
filterbank_features = filterbank_features.T
plt.matshow(filterbank_features)
plt.title('Filter bank')
plt.show()