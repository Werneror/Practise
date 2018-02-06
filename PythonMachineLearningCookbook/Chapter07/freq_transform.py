# ^_^ coding:utf-8 ^_^

import numpy as np 
from scipy.io import wavfile
import matplotlib.pyplot as plt 

# 读取输入文件
sampling_freq, audio = wavfile.read('input_freq.wav')

# 标准化数值
audio = audio / (2.0**15)

# 提取数组长度
len_audio = len(audio)

# 应用傅立叶变换
transformed_signal = np.fft.fft(audio)
half_length = np.ceil((len_audio+1)/2.0)
transformed_signal = abs(transformed_signal[0:int(half_length)])
transformed_signal /= float(len_audio)
transformed_signal **= 2

# 提取转换信号长度
len_ts = len(transformed_signal)

# 将部分信号和乘以2
if len_audio % 2:
    transformed_signal[1:len_ts] *= 2
else:
    transformed_signal[1:len_ts-1] *= 2

# 获取功率信号
power = 10*np.log10(transformed_signal)

# 建立时间轴
x_values = np.arange(0, half_length, 1) * \
                           (float(sampling_freq)/len_audio) / 1000.0

# 画图
plt.figure()
plt.plot(x_values, power, color='black')
plt.xlabel('Freq (in kHz)')
plt.ylabel('Power (in dB)')
plt.show()
