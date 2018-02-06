# ^_^ coding:utf-8 ^_^

import numpy as np 
import matplotlib.pyplot as plt 
from scipy.io import wavfile

# 读取输入文件
sampling_freq, audio = wavfile.read('input_read.wav')

# 打印参数
print(u"Shape: {}\nDatatype: {}\nDuration: {:.3f} seconds".format(
    audio.shape, audio.dtype, audio.shape[0]/float(sampling_freq)))

# 标准化数值
audio = audio / (2.0**15)

# 提取前300个值画图
audio = audio[:300]

# 建立时间轴
x_values = np.arange(0, len(audio), 1) / float(sampling_freq)

# 将单位转换成毫秒
x_values *= 1000

# 画出声音信号图
plt.plot(x_values, audio, color='black')
plt.xlabel('Time (ms)')
plt.ylabel('Amplitude')
plt.title('Audio signal')
plt.show()