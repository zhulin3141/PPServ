#!/usr/bin/env python
# coding:utf-8

from base_module import *
from mod_memcached import *
from mod_apache import *
from mod_php import *
from mod_mysql import *
from conf import *

class ModuleFactory():
    '''模块工厂类

    根据分组生成模块
    '''
    @staticmethod
    def factory(name):
        group = BaseModule.list_module_data()[name]['group']
        if group == "memcached":
            return Mod_Memcached(name)
        elif group == "apache":
            return Mod_Apache(name)
        elif group == "php":
            return Mod_Php(name)
        elif group == "mysql":
            return Mod_Mysql(name)
        else:
            return BaseModule(name)

    @staticmethod
    def get_module_list(service_list=None):
        list = []
        if service_list is None:
            service_list = Conf().get('module')
        for module_name in service_list:
            list.append(ModuleFactory.factory(module_name))
        return list
