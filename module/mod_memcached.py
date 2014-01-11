from comm import *
from module.module import *
from tkinter import *
from tkinter.ttk import *

class Mod_Memcached(Module):
    '''Memcached模块类'''
    def __init__(self, name):
        Module.__init__(self, name)

    def install_service(self):
        '''安装服务后根据配置中的数据修改memcached服务的数据'''
        result = Module.install_service(self)
        execute("sc description %s \"%s\"" % (self.service_name, self.service_name))
        return result


    def set_advt_frame(self,parent,fun):
        mem_tab = Frame(parent)
        parent.add(mem_tab, text=self.module_name)
