#!/usr/bin/python2.7
# ^_^ coding:utf8 ^_^

import string
import base64


def rot13(oristr):

    dststr = []
    upperdict = {}
    lowerdict = {}
    upperletters = string.ascii_uppercase
    lowerletters = string.ascii_lowercase

    for i in range(0, len(lowerletters)):
        if i < 13:
            lowerdict[lowerletters[i]] = lowerletters[i + 13]
        else:
            lowerdict[lowerletters[i]] = lowerletters[i - 13]

    for i in range(0, len(upperletters)):
        if i < 13:
            lowerdict[upperletters[i]] = upperletters[i + 13]
        else:
            lowerdict[upperletters[i]] = upperletters[i - 13]

    for ch in oristr:
        if ch in lowerdict:
            dststr.append(lowerdict[ch])
        elif ch in upperdict:
            dststr.append(upperdict[ch])
        else:
            dststr.append(ch)

    return ''.join(dststr)


def decode(s):
    ret = ''
    for c in s:
        c = chr(ord(c) - 1)
        ret += c
    return ret


if __name__ == '__main__':
    input_string = "a1zLbgQsCESEIqRLwuQAyMwLyq2L5VwBxqGA3RQAyumZ0tmMvSGM2ZwB4tws"
    output_rot13 = rot13(input_string)
    output_rev = output_rot13[::-1]
    output_base64 = base64.b64decode(output_rev)
    output_decode = decode(output_base64)
    print(output_decode[::-1])
