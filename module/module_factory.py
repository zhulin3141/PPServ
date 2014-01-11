from module.mod_memcached import *
from module.mod_apache import *
from module.mod_php import *
from module.mod_mysql import *
from module.module import *

class ModuleFactory():
    '''模块工厂类

    根据分组生成模块
    '''
    @staticmethod
    def factory(name):
        group = Conf().get('module')[name]['group']
        if group == "memcached":
            return Mod_Memcached(name)
        elif group == "apache":
            return Mod_Apache(name)
        elif group == "php":
            return Mod_Php(name)
        elif group == "mysql":
            return Mod_Mysql(name)
        else:
            return Module(name)
