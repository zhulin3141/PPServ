#!/usr/bin/env python
# coding:utf-8

from common import *
from base_module import BaseModule
from lang import *
import wx

class Mod_Mysql(BaseModule):
    '''Mysql模块类'''
    def __init__(self, name):
        BaseModule.__init__(self, name)

    def set_advt_frame(self, parent):
        mysqlPanel = wx.Panel(parent.advtTab)
        parent.advtTab.AddPage(mysqlPanel, self.module_name)

        consoleBtn = wx.Button(mysqlPanel, -1, Lang().get('console'))
        consoleBtn.Bind(wx.EVT_BUTTON, self.open_console)

    def open_console(self, event):
        os.system('start /D "%s" mysql -u root' % (BASE_DIR + self.path + '\\bin'))