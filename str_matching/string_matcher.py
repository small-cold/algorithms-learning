#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    字符匹配的几种算法实现，待匹配字符串均已数组作为参数，如果数组size = 1,
    就是标准的算法实现了，之所以添加数组，是因为遇到一个匹配敏感词的需求，
    都是要匹配多个字符串，找到这些命中的词
"""


def naive(source, targets=[]):
    """
    朴素算法，对目标词，使用find方法逐个匹配，
    时间复杂度 O(n-m +1)m, n为待匹配词长度，m为目标词长度
    此方法，还要乘以目标词的数量，效率极低
    :param source:
    :param targets:
    :return:
    """
    match_result = []
    for t in targets:
        if source.find(t) >= 0:
            match_result.append(t)
    return match_result


def rabin_carp_all(source, targets=[]):
    """
    Rabin-Carp 算法，匹配包含多个字符串中的哪一些
    :param source:
    :param targets:
    :return:
    """
    match_result = []
    for target in targets:
        result = rabin_carp(source, target)
        if result:
            match_result.append(result)
    return match_result


def rabin_carp(source, target, q=13, d=10):
    """
    Rabin-Carp 算法，每个字符看做是10禁止的数，然后对某个数取膜，
    如果模相等则有可能是目标字符串，然后做进一步验证
    时间复杂度为O(n-m +1)m，但基于假设的情况，通常情况比朴素算法要好
    :param d: 字符转化为数字的基数
    :param q: 素数，用于取膜
    :param target: 目标词
    :param source: 待匹配词
    :return:
    """
    n = len(source)
    m = len(target)
    if m == n:
        return source if source == target else None
    elif m > n:
        return None
    h = d ^ (m - 1) % q
    p = 0
    t = 0
    for tg in target:
        p = (d * p + ord(tg)) % q
        t = (d * t + ord(tg)) % q
    for s in range(n - m):
        if p == t:
            if target == source[s: m]:
                return target
        if s < n - m:
            t = (d * (t - ord(source[s]) * h)) + ord(source[s + m]) % q
    return None


def finite_automaton(source=[], targets=[]):
    """
    有限自动机算法，也是正则的实现
    :param targets: 目标词
    :param source: 待匹配词
    :return:
    """
    # 构造数据结构，类似于正则的解析
    return ComputeTransition(targets).find_all(source)


class ComputeTransition(object):
    """
    字符串有限自动机实现类
    """

    def __init__(self, targets):
        self.targets = targets
        self.pattern = {}
        self.init_pattern()

    def init_pattern(self):
        """
        初始化自动机
        """
        for target in self.targets:
            node = self.pattern
            prefix = ''
            for t in target:
                prefix += t
                # 取子节点
                sub_node = node.get(t, None)
                # 如果子节点不存在，则创建新的
                if not sub_node:
                    sub_node = {'is_end': False,
                                'target': prefix}
                    node[t] = sub_node
                if prefix == target:
                    sub_node['is_end'] = True
                node = sub_node

    def find_all(self, source):
        """
        找到所有符合模式的匹配字符串
        :param source:
        :return:
        """
        results = []
        last_status_list = None
        for i in source:
            # 获取状态集合
            last_status_list = self.get_new_status_list(last_status_list, i)
            for status in last_status_list:
                if status:
                    if status.get("is_end", False):
                        results.append(status.get("target", ""))
        return results

    def get_new_status_list(self, last_list, i):
        """
        根据上一次的状态集合，获取下一次的状态集合
        :param last_list:
        :param i:
        :return:
        """
        new_list = []
        # 考虑是否符合第一个输入
        root = self.pattern.get(i, None)
        if root:
            new_list.append(root)

        # 上一次的状态不是空，则获取下一次状态
        if last_list:
            for last in last_list:
                new_status = last.get(i, None)
                if new_status:
                    new_list.append(new_status)
        return new_list


def kunth_morris_pratt(source, targets=[]):
    """
    简称KMP算法，线性时间算法
    :param source:
    :param targets:
    :return:
    """
    match_result = []

    return match_result


if __name__ == '__main__':
    print(finite_automaton("aaaababcabbdd", ['aba', 'abc', 'ababab', 'aaaa']))

