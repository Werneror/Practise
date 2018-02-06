# ^_^ coding:utf-8 ^_^

########################
#没有找到数据源，未运行此程序#
########################

import os
import argparse
import numpy as np 
from scipy.io import wavfile
from hmmlearn import hmm
from python_speech_features import mfcc

# 创建类处理HMM相关过程
class HMMTrainer(object):

    def __init__(self,
                        model_name='GaussianHMM',
                        n_components=4, #隐藏状态个数
                        cov_type='diag', #转移矩阵的协方差类型
                        n_iter=1000 #训练的迭代次数
                        ):

        self.model_name = model_name
        self.n_components = n_components
        self.cov_type = cov_type
        self.n_iter = n_iter
        self.models = []
        
        if self.model_name == 'GaussianHMM':
            self.model = hmm.GaussianHMM(
                                            n_components = self.n_components,
                                            covariance_type = self.cov_type,
                                            n_iter=self.n_iter)
        else:
            raise TypeError('Invalid model type')

    # X是二维数组，其中每一行是13维
    def train(self, X):
        np.seterr(all='ignore')
        self.models.append(self.model.fit(X))

    # 对输入数据运行模型
    def get_score(self, input_data):
        return self.model.score(input_data)

# 解析输入参数的函数
def build_arg_parser():
    parser = argparse.ArgumentParser(description='Trains the HMM classifier')
    parser.add_argument("--input-folder", dest="input_folder", required=True, help="Input folder containing the audio files insubfolders")
    return parser

if __name__ == '__main__':
    args = build_arg_parser().parse_args()
    input_folder = args.input_folder

    # 初始化隐马尔可夫模型的变量
    hmm_models = []

    # 解析输入路径
    for dirname in os.listdir(input_folder):

        #获取子文件夹名称
        subfolder = os.path.join(input_folder, dirname)
        if not os.path.isdir(subfolder):
            continue

        #提取标记
        label = subfolder[subfolder.rfind('/')+1:]

        # 初始化用于训练的变量
        X = np.array([])
        y_words = []

        # 迭代所有音频文件
        for filename in [x for x in os.listdir(subfolder) if x.endswith('.wav')][:-1]:

            # 读取每个音频文件
            filepath = os.path.join(subfolder, filename)
            sampling_freq, audio = wavfile.read(filepath)

            # 提取MFCC特征
            mfcc_features = mfcc(audio, sampling_freq)

            # 将MFCC特征添加到X变量
            if len(X) == 0:
                X = mfcc_features
            else:
                X = np.append(X, mfcc_features, axis =0)

            # 添加标记
            y_words.append(label)

        # 训练并保存HMM模型
        hmm_trainer = HMMTrainer()
        hmm_trainer.train(X)
        hmm_models.append((HMMTrainer, label))
        hmm_trainer = None

    # 测试文件
    input_files = [
            'data/pineapple/pineapple15.wav',
            'data/orange/orange15.wav',
            'data/apple/apple15.wav',
            'data/kiwi/kiwi15.wav']

    # 为输入数据分类
    for input_file in input_files:

            # 读取每个音频文件
            sampling_freq, audio = wavfile.read(input_file)

            # 提取MFCC特征
            mfcc_features = mfcc(audio, sampling_freq)

            # 定义变量
            max_score = None
            output_label = None

            # 迭代所有HMM模型并取得分最高者
            for item in hmm_models:
                hmm_model, label = item
                score = hmm_model.get_score(mfcc_features)
                if score > max_score:
                    max_score = score
                    output_label = label
    
    # 打印结果
    print(u"输入：{}".format(input_file[input_file.find('/')+1:input_file.rfiend('/')]))
    print(u"预测：{}".format(output_label))