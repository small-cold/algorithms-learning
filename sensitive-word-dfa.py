#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time

"""
    使用DFA 有限自动机算法实现。
    路劲根据需要修改
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

# 完全命中敏感词队列
full_hit_result = []
# 部分命中敏感词队列
part_hit_result = []
# 未命中敏感词队列
normal_result = []


# 读取敏感词到内存
def read_sensitive():
    print("正在读取敏感词....")
    root = {}
    with open(PATH_SENSITIVE, 'r') as f:
        for line in f.readlines():
            word = line.strip()
            node = root
            index = 0
            for c in word:
                index += 1
                # 取子节点
                sub_node = node.get(c, None)
                # 如果子节点不存在，则声明新的
                if not sub_node:
                    sub_node = {'is_end': False}
                    node[c] = sub_node
                if index == len(word):
                    sub_node['is_end'] = True
                node = sub_node

    print("敏感词读取完成")
    return root


def deal_source(sensitive_tree, begin=0, end=0):
    print("开始处理关键词....")
    index = 0
    with open(PATH_SOURCE, 'r') as f:
        for line in f.readlines():
            index += 1
            if begin > 0 and index <= begin:
                continue
            check_sensitive(line.strip(), sensitive_tree, "第" + str(index) + "行：")
            if index > end > 0:
                break
    print("关键词处理完成")


def check_sensitive(keyword, sensitive_tree, name=''):
    if not sen_root:
        print("敏感词为空")
        return

    # print('%s thread %s is dealing keyword %s ' % (index, threading.current_thread().name, keyword))
    write_queue = normal_result
    hit_word = ''
    node = sensitive_tree
    for c in keyword:
        node = node.get(c, None)
        # 如果为空，继续下一个字符
        if not node:
            node = sensitive_tree
            continue
        hit_word += c
        if node.get('is_end', False):
            # 匹配到了，是否等于敏感词
            print(name, '【', keyword, "】命中敏感词：", hit_word)
            if keyword == hit_word:
                write_queue = full_hit_result
            else:
                write_queue = part_hit_result
            hit_word += ","

    write_queue.append(keyword + "\n")


def write_result(results, path):
    print("正在执行写入文件操作:", path)
    with open(path, 'w') as f:
        for a in results:
            f.write(a)
    print("写入文件操作结束:", path)


if __name__ == '__main__':
    start = time.time()
    sen_root = read_sensitive()
    print("读取敏感词结束，已耗时：", str(time.time() - start), "开始检查词库...")
    deal_source(sen_root)
    print("查词库完成，已耗时：", str(time.time() - start), "开始写入文件...")
    write_result(full_hit_result, PATH_FULL_HIT)
    write_result(part_hit_result, PATH_PART_HIT)
    write_result(normal_result, PATH_NORMAL)
    print("数据处理完成，写入文件完成，总计耗时", str(time.time() - start))
