#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime as dt

from str_matching import string_matcher
from util import file_util

# 根路径
PATH_ROOT = "/Users/Chao/Desktop/"
# 待处理词路径
PATH_SOURCE = PATH_ROOT + "待过滤的词.txt"
# 敏感词库
PATH_SENSITIVE = PATH_ROOT + "和谐词.txt"
# 完全命中敏感词的词
PATH_FULL_HIT = PATH_ROOT + "完全命中.txt"
# 部分命中敏感词
PATH_PART_HIT = PATH_ROOT + "部分命中.txt"
# 正常结果
PATH_NORMAL = PATH_ROOT + "正常词.txt"

if __name__ == '__main__':
    # ps: 实际使用时，这样读取文件对内存要求较高，应该边读边处理
    # 读取文件
    start_time = dt.now()
    harmonious_words = file_util.read_txt(PATH_SENSITIVE, limit=50000)
    source_words = file_util.read_txt(PATH_SOURCE, limit=200000)
    print("读取文件耗时(ms)：", dt.now() - start_time)
    # 朴素算法
    print("开始进行朴素算法：")
    start_time = dt.now()
    # 1000 匹配 10000 个词的耗时 2.1s 左右
    for source in source_words:
        string_matcher.naive(source, harmonious_words)
    print("朴素算法耗时：", dt.now() - start_time)

    print("开始进行Rabin-Carp 算法：")
    start_time = dt.now()
    for source in source_words:
        string_matcher.rabin_carp_all(source, harmonious_words)
    print("进行Rabin-Carp 算法耗时", dt.now() - start_time)

    print("开始进行有限自动机算法：")
    start_time = dt.now()
    # 把预处理过程，即构建自动机的步骤，提取出来，才能提高效率
    computeTransition = string_matcher.ComputeTransition(harmonious_words)
    for source in source_words:
        find = computeTransition.find_all(source)
    print("进行有限自动机算法耗时", dt.now() - start_time)
