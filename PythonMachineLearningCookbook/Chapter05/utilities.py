# ^_^ coding:utf-8 ^_^

import numpy as np
import matplotlib.pyplot as plt
from sklearn import cross_validation

def load_data(input_file):
    X = []
    with open(input_file, 'r') as f:
        for line in f.readlines():
            data = [float(x) for x in line.split(',')]
            X.append(data)
    return np.array(X)