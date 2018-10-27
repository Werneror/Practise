# ^_^ coding:utf8 ^_^
#! /usr/bin/python2
#! /usr/bin/python3

'''
同时从命令行参数和标准输入读取输入
```
echo -e 'a\nb\nc' | python argv_stdin.py
```
和
```
python argv_stdin.py a b c
```
的输出都是
```
inputline: a
inputline: b
inputline: c
```
'''

import sys
import select


def input_from_stdin():
    targets = list()
    while sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
        line = sys.stdin.readline()
        if line:
            targets.append(line.rstrip('\n'))
        else:
            break
    return targets


def input_from_argv():
    return sys.argv[1:]


def get_input():
    return input_from_argv() + input_from_stdin()


if __name__ == '__main__':
    for target in get_input():
        print('inputline: {}'.format(target))
