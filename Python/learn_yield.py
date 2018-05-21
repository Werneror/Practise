#!/usr/bin/python
# ^_^ coding:utf8 ^_^
# 阅读[《Python yield 使用浅析 》](https://www.ibm.com/developerworks/cn/opensource/os-cn-python-yield/)
# 后写的用于巩固学习成果的代码，在Python3.6中运行通过

from collections import Iterable
from inspect import isgeneratorfunction

def fab1(max):
    '''直接打印版'''
    n, a, b = 0, 0, 1
    while n < max:
        print(b)
        a, b = b, a+b
        n += 1

def fab2(max):
    '''返回list版'''
    ret = list()
    n, a, b = 0, 0, 1
    while n < max:
        ret.append(b)
        a, b = b, a+b
        n += 1
    return ret

class Fab3():
    '''可迭代类版'''
    def __init__(self, max):
        self.max = max
        self.n, self.a, self.b = 0, 0, 1

    def __iter__(self):
        return self

    def __next__(self):
        if self.n < self.max:
            r = self.b
            self.a, self.b = self.b, self.a + self.b
            self.n += 1
            return r
        else:
            raise StopIteration()

def fab4(max):
    '''yield版'''
    n, a, b = 0, 0, 1
    while n < max:
        yield b
        a, b = b, a+b
        n += 1

if __name__ == '__main__':

    print(fab1.__doc__)
    fab1(5)
    print(fab2.__doc__)
    for num in fab2(5):
        print(num)
    print(Fab3.__doc__)
    for num in Fab3(5):
        print(num)
    print(fab4.__doc__)
    for num in fab4(5):
        print(num)

    print("fab4是生成器吗？\t{}".format(isgeneratorfunction(fab4)))
    print("fab4(5)是生成器吗？\t{}".format(isgeneratorfunction(fab4(5))))
    print("fab4是可迭代的吗？\t{}".format(isinstance(fab4, Iterable)))
    print("fab4(5)可迭代吗？\t{}".format(isinstance(fab4(5), Iterable)))
