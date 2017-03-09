#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import queue
import threadpool

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

# PATH_LOG = open("/Users/Chao/Desktop/查询敏感词日志.log", 'a')

full_hit_result = queue.Queue()
part_hit_result = queue.Queue()
normal_result = queue.Queue()


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


pool_write = threadpool.ThreadPool(3)
# pool_read = threadpool.ThreadPool(20)


def deal_source(sen_root, begin=0, end=0):
    print("开始处理关键词....")
    index = 0
    with open(PATH_SOURCE, 'r') as f:
        for line in f.readlines():
            index += 1
            if begin > 0 and index <= begin:
                continue
            check_sensitive(line.strip(), sen_root, "第" + str(index) + "行：")
            if index > end > 0:
                break
    print("关键词处理完成")


def check_sensitive(keyword, sen_root, name=''):
    if not sen_root:
        print("敏感词为空")
        return

    # print('%s thread %s is dealing keyword %s ' % (index, threading.current_thread().name, keyword))
    write_queue = normal_result
    hit_word = ''
    node = sen_root
    for c in keyword:
        node = node.get(c, None)
        # 如果为空，继续下一个字符
        if not node:
            node = sen_root
            continue
        hit_word += c
        if node.get('is_end', False):
            # 匹配到了，是否等于敏感词
            hit_word += ","
            print(name, '【', keyword, "】命中敏感词：", hit_word)
            if keyword == hit_word:
                write_queue = full_hit_result
            else:
                write_queue = part_hit_result

    write_queue.put(keyword + "\n")


def write_result(results, path):
    print("正在执行写入文件操作:", path)
    with open(path, 'w') as f:
        while not results.empty():
            try:
                result = results.get(timeout=1)
                if result is not None:
                    f.write(result)
            except Exception as e:
                print("写入文件操作异常，等待3秒", e)
                time.sleep(3)
    print("写入文件操作结束:", path)


if __name__ == '__main__':
    start = time.time()
    root = read_sensitive()
    # check_sensitive("售麻醉大量号码出售", root)
    # 开启写线程，等待
    requests = threadpool.makeRequests(write_result, [([full_hit_result, PATH_FULL_HIT], None),
                                                      ([part_hit_result, PATH_PART_HIT], None),
                                                      ([normal_result, PATH_NORMAL], None)])
    [pool_write.putRequest(req) for req in requests]
    # 开始处理数据
    deal_source(root)
    # todo 写文件这里有问题，没有正常结束，还没搞清楚，线程池怎么判断结束
    # pool_read.joinAllDismissedWorkers()
    pool_write.wait()
    print("处理完成，耗时", str(time.time() - start))
