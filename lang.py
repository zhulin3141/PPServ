#!/usr/bin/env python
# coding:utf-8

from common import *

@singleton
class Lang(object):
    '''
    语言加载类
    
    Attributes:
        data: 加载的数据
        language: 加载的语言文件名称
    '''

    language = 'zh_cn'

    def __init__(self):
        self.langfile = 'lang/%s.json' % self.language
        self.data = self.load()

    def get(self, name=None):
        if( name is None ):
            return self.data
        else:
            return self.data[name]

    def load(self):
        '''加载语言文件数据'''
        return load_json(self.langfile)
