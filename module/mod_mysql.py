from comm import *
from module.module import *
from tkinter import *
from tkinter.ttk import *

class Mod_Mysql(Module):
    '''Mysql模块类'''
    def __init__(self, name):
        Module.__init__(self, name)

    def set_advt_frame(self,parent,fun):
        mysql_tab = Frame(parent)
        parent.add(mysql_tab, text=self.module_name)