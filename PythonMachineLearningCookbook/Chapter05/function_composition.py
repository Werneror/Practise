# ^_^ coding:utf-8 ^_^

import numpy as np

def add3(input_array):
    return map(lambda x: x+3, input_array)

def mul2(input_array):
    return map(lambda x: x*2, input_array)

def sub5(input_array):
    return map(lambda x: x-5, input_array)

def function_composer(*args):
    return reduce(lambda f,g:lambda x:f(g(x)), args)

if __name__ == '__main__':
    arr = np.array([2, 5, 4, 7])
    print(u"输入：{}\n".format(arr))

    print(u"操作：sub5(mul2(add3(arr)))")

    # 常规方法
    arr1 = add3(arr)
    arr2 = mul2(arr1)
    arr3 = sub5(arr2)
    print(u"常规方法输出为：{}".format(arr3))

    # 高级方法
    func_composed = function_composer(sub5, mul2, add3)(arr)
    print(u"高级方法输出为：{}\n".format(func_composed))

    # 另一个高级方法的例子    
    print(u"操作：mul2(sub5(mul2(add3(sub5(arr)))))")
    func_composed = function_composer(mul2, sub5, mul2, add3, sub5)(arr)
    print(u"高级方法输出为：{}\n".format(func_composed))    