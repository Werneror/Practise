# ^_^ coding:utf-8 ^_^

import numpy as np 
import matplotlib.pyplot as plt 
from scipy.io.wavfile import write

# 定义存储音频的输出文件
output_file = 'output_generated.wav'

# 指定音频生成参数
duration = 3                   #单位s
sampling_freq = 44100 #单位Hz
tone_freq = 587
min_val = -2*np.pi
max_val = 2*np.pi

# 生成音频信号
t = np.linspace(min_val, max_val, duration*sampling_freq)
audio = np.sin(2*np.pi*tone_freq*t)

# 增加噪声
noise = 0.4 * np.random.rand(duration*sampling_freq)
audio += noise

# 转换为16位整型数
scaling_factor = pow(2, 15) - 1
audio_normalized = audio / np.max(np.abs(audio))
audio_scaled = np.int16(audio_normalized*scaling_factor)

# 写入输出文件
write(output_file, sampling_freq, audio_scaled)

# 用前100个值画出该信号
audio = audio[:100]

# 生成时间轴
x_values = np.arange(0, len(audio), 1) / float(sampling_freq)

# 将时间轴单位转换为毫秒
x_values *= 1000

# 画出音频信号图
plt.plot(x_values, audio, color='black')
plt.xlabel('Time (ms)')
plt.ylabel('Amplitude')
plt.title('Audio signal')
plt.show()