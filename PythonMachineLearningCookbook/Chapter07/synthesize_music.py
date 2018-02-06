# ^_^ coding:utf-8 ^_^

import json
import numpy as np 
from scipy.io.wavfile import write
import matplotlib.pyplot as plt 

# 定义合成音调
def synthesizer(freq, duration, amp=1.0, sampling_freq=44100):

    # 建立时间轴
    t = np.linspace(0,duration, duration*sampling_freq)

    # 构建音频信号
    audio = amp*np.sin(2*np.pi*freq*t)

    return audio.astype(np.int16)

if __name__ == '__main__':

    # 读取频率映射文件
    tone_map_file = 'tone_freq_map.json'
    with open(tone_map_file, 'r') as f:
        tone_freq_map = json.loads(f.read())

    ### 生成2s的G调 ###

    # 设置生成G调输入参数
    input_tone = 'G'             #声音频率
    duration = 2                   #时长
    amplitude = 10000        #振幅
    sampling_freq = 44100 #采样频率

    # 生成音阶
    synthesized_tone = synthesizer(tone_freq_map[input_tone],
                                                          duration,
                                                          amplitude,
                                                          sampling_freq)

    # 写入输出文件
    write('output_tone.wav', sampling_freq, synthesized_tone)

    ### 生成音乐 ###

    # 定义音阶及持续时间
    tone_seq = [('D', 0.3), ('G', 0.6), ('C', 0.5), ('A', 0.3), ('Asharp', 0.7)]

    # 构建基于和弦序列的音频信号
    output = np.array([])
    for item in tone_seq:
        input_tone = item[0]
        duration = item[1]
        synthesized_tone = synthesizer(tone_freq_map[input_tone],
                                                              duration,
                                                              amplitude,
                                                              sampling_freq)
        output = np.append(output, synthesized_tone, axis=0)

    # 写入输出文件
    write('output_tone_seq.wav', sampling_freq, output)