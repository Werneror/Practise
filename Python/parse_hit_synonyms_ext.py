#!/user/bin/env python3
# -*- coding:utf-8 -*-
# 解析哈工大信息检索研究室同义词词林扩展版，生成 JSON 格式文件
import json


def decode_index(header):
    """
    解析每行开头的索引。
    索引类似于 Aa01C12=
    第一位 A 表示第 1 级，大类
    第二位 a 表示第 2 级，中类
    第三、四位 01 表示第 3 级，小类
    第五位 C 表示第 4 级，词群
    第六、七位 12 表示第 5 级，原子词群
    最八位含义为：= 代表同义词，# 相关词语，@ 代表它在词典中既没有同义词，也没有相关词
    """
    if len(header) != 8:
        raise RuntimeError(f'Invalid header {header}')
    return header[0], header[1], header[2:4], header[4], header[5:7], header[7]


def get_group(synonyms, index):
    group = synonyms
    for i in range(0, 4):
        if index[i] not in group:
            group[index[i]] = dict()
        group = group[index[i]]
    return group


def parse_hit_synonyms_ext(path, encoding):
    """
    解析同义词扩展词典。词典中每一行是一些同义词或相关词语。词典中的行示例：
    Aa01A01= 人 士 人物 人士 人氏 人选
    Aa01A02= 人类 生人 全人类
    Aa01A03= 人手 人员 人口 人丁 口 食指
    Aa01A04= 劳力 劳动力 工作者
    """
    synonyms = dict()
    with open(path, encoding=encoding) as f:
        for line in f:
            words = line.strip().split(' ')
            index = decode_index(words[0])
            words = words[1:]
            group = get_group(synonyms, index)
            group[index[4]] = {"words": words, "type": index[5]}
    return synonyms


if __name__ == '__main__':
    synonyms = parse_hit_synonyms_ext('哈工大社会计算与信息检索研究中心同义词词林扩展版.txt', 'gbk')
    with open('hit_synonyms_ext.json', 'w', encoding='utf-8') as f:
        json.dump(synonyms, f, ensure_ascii=False)
