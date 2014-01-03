#!/usr/bin/env python
# coding:utf-8

from common import *
from base_module import BaseModule

class Mod_Memcached(BaseModule):
    '''Memcached模块类'''
    def __init__(self, name):
        BaseModule.__init__(self, name)

    def install_service(self):
        '''安装服务后根据配置中的数据修改memcached服务的数据'''
        result = super().install_service(self)
        execute("sc description %s \"%s\"" % (self.service_name, self.service_name))
        return result
