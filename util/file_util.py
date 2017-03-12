#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def read_txt(path, start=0, limit=0):
    """
    读取TXT文本文件工具类
    :param limit: 限制读取的行数，默认为0不限
    :param start: 限制起始的位置，默认为0，从头开始
    :param path: 路径
    :return: 结果集合
    """
    result = []
    print("正在读取文件....", end="\r")
    index = 0
    with open(path, 'r') as f:
        for line in f.readlines():
            index += 1
            if index <= start:
                continue
            if limit > 0 and index > limit + start:
                break
            result.append(line.strip())  # 把末尾的'\n'删掉
    print("读取文件完成", path)
    return result


def write_txt(path, contents):
    """
    写入文本文件，自动在结尾添加换行
    :param path:
    :param contents:
    :return:
    """
    print("正在写入文件....", path, end="\r")
    with open(path, 'w') as f:
        for s in contents:
            f.write(s + "\n")
    print("写入文件完成", path, end="\r")
