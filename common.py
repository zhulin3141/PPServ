#!/usr/bin/env python
# coding:utf-8

import re
import codecs
import json
import collections


def singleton(cls, *args, **kw):
    instances = {}
    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]
    return _singleton

comment_re = re.compile(
    '(^)?[^\S\n]*/(?:\*(.*?)\*/[^\S\n]*|/[^\n]*)($)?',
    re.DOTALL | re.MULTILINE
)

def load_json(file_path):
    '''解析json文件
    首先去除注释再用json模块
    注释示例：
        //...
        或
        /*
        ...
        */
    '''
    with codecs.open(file_path,'r','utf-8') as file:
        content = ''.join(file.readlines())

        match = comment_re.search(content)
        while match:
            content = content[:match.start()] + content[match.end():]
            match = comment_re.search(content)

        return json.loads(content, object_pairs_hook=collections.OrderedDict)
