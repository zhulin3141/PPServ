#!/usr/bin/env python
# coding:utf-8

from common import *
from conf import *


@singleton
class Cache():
    """缓存类

    Attributes:
        cache_file: 缓存文件
        data: 缓存的数据
    """

    cache_file = 'data/bin.dat'
    data = {}

    def __init__(self):
        #没有数据则设置默认的数据
        self.load()
        if len(self.data) is 0:
            self.set_default()

    def set(self, key, value):
        """设置并写入数据

        Args:
            key: 写入的关键字
            value: 对应的数据
        """
        self.data[key] = value
        self.write()

    def get(self, key=None):
        """获取数据

        Args：
            key: 获取数据的关键字
        """
        if key:
            return self.data[key]
        else:
            return self.data

    def load(self):
        """加载数据"""
        self.data = load_json(self.cache_file)

    def write(self):
        """保存数据"""
        with open(self.cache_file, 'w') as cf:
            cf.write(json.dumps(self.data))

    def set_default(self):
        """设置默认的缓存数据并写入"""
        default = {
            "autorun": {}
        }

        modules = Conf().get('module')
        for autorun_name in modules.keys():
            default['autorun'][autorun_name] = 1

        self.data = default
        self.write()

    def clear(self):
        """清空数据"""
        self.data = {}
        self.write()
