#!/usr/bin/env python
# coding:utf-8

from common import *
from base_module import BaseModule
from lang import *
import wx
import os

class Mod_Memcached(BaseModule):
    '''Memcached模块类'''
    def __init__(self, name):
        BaseModule.__init__(self, name)

    def install_service(self):
        '''安装服务后根据配置中的数据修改memcached服务的数据'''
        result = super(Mod_Memcached, self).install_service()
        execute("sc description %s \"%s\"" % (self.service_name, self.service_name))
        return result

    def set_advt_frame(self, parent):
        self.setting_panel = wx.Panel(parent)
        parent.AddPage(self.setting_panel, self.module_name)

        consoleBtn = wx.Button(self.setting_panel, -1, Lang().get('console'))
        consoleBtn.Bind(wx.EVT_BUTTON, self.open_console)

    def open_console(self, event):
        os.system('start /D "%s"' % (BASE_DIR + self.path))