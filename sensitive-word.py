#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time

"""
    单线程简单实现
    待比对词N个，敏感词为M个，时间复杂度为O(M * N)
    时间复杂度呈指数级递增
"""
# 待处理词路径
PATH_SOURCE = "/Users/Chao/Desktop/关键词20170308.txt"
# 敏感词库
PATH_SENSITIVE = "/Users/Chao/Desktop/违禁词.txt"

# 完全命中敏感词的词
PATH_FULL_HIT = "/Users/Chao/Desktop/完全命中.txt"
# 部分命中敏感词
PATH_PART_HIT = "/Users/Chao/Desktop/部分命中.txt"
# 正常结果
PATH_NORMAL = "/Users/Chao/Desktop/正常词.txt"

PATH_LOG = "/Users/Chao/Desktop/查询敏感词日志.log"

sensitive_wordlist = []
full_hit_result = []
part_hit_result = []
normal_result = []


# 读取敏感词到内存
def read_sensitive():
    print("正在读取敏感词....")
    with open(PATH_SENSITIVE, 'r') as f:
        for line in f.readlines():
            sensitive_wordlist.append(line.strip())  # 把末尾的'\n'删掉
    print("敏感词读取完成")


def deal_source():
    print("开始处理关键词....")
    index = 0
    with open(PATH_SOURCE, 'r') as f:
        for line in f.readlines():
            index += 1
            keyword = line.strip()  # 去掉结尾的换行
            check_sensitive(keyword, index)
    print("关键词处理完成")


def check_sensitive(keyword, index):
    # print('%s thread %s is dealing keyword %s ' % (index, threading.current_thread().name, keyword))
    has_sensitive = False
    for sensitive_word in sensitive_wordlist:
        if keyword == sensitive_word:
            full_hit_result.append(keyword + "\n")
            has_sensitive = True
            print(index, "完全命中。关键词：", keyword, "，敏感词：", sensitive_word, end="\n", file=PATH_LOG)
            break
        elif keyword.find(sensitive_word) >= 0:
            part_hit_result.append(keyword + "\n")
            has_sensitive = True
            print(index, "部分命中。关键词：", keyword, "，敏感词：", sensitive_word, end="\n", file=PATH_LOG)
            break
    # 如果没有敏感词，写入正常词文件
    if not has_sensitive:
        print(index, "未命中。关键词：", keyword, end="\n")
        normal_result.append(keyword + "\n")


if __name__ == '__main__':
    start = time.time()
    read_sensitive()
    # 开始处理数据
    deal_source()
    print("开始写文件。。。。")
    with open(PATH_PART_HIT, 'w') as f:
        for s in part_hit_result:
            f.write(s)
    with open(PATH_FULL_HIT, 'w') as f:
        for s in full_hit_result:
            f.write(s)
    with open(PATH_NORMAL, 'w') as f:
        for s in normal_result:
            f.write(s)
    print("处理完成，耗时", str(time.time() - start))
