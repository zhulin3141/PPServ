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
        self.conf_file = BASE_DIR + self.path + "\my.ini"
        self.parse_config_file()

    def parse_config_file(self):
        pass

    def set_advt_frame(self, parent):
        self.setting_panel = wx.Panel(parent)
        self.setting_panel.SetSizer(self.setting_sizer)

        self.opt_sizer = wx.BoxSizer(wx.VERTICAL)
        self.grid_sizer = wx.FlexGridSizer(rows=15, cols=2)

        conf_btn = wx.Button(self.setting_panel, -1, Lang().get('mysql_config_file'))
        conf_btn.Bind(wx.EVT_BUTTON, self.open_config_file)

        consoleBtn = wx.Button(self.setting_panel, -1, Lang().get('console'))
        consoleBtn.Bind(wx.EVT_BUTTON, self.open_console)

        self.handler_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.handler_sizer.AddMany([
            (conf_btn),
            (consoleBtn)
        ])

        self.opt_sizer.Add(self.grid_sizer)
        self.opt_sizer.Add(self.handler_sizer, 0, wx.TOP, 5)
        self.setting_sizer.Add(self.opt_sizer, 0, wx.ALL, 5)

        parent.AddPage(self.setting_panel, self.module_name)

    def open_config_file(self, event):
        open_file(self.conf_file)

    def open_console(self, event):
        open_cmd(self.path + '\\bin', 'mysql -u root -p')
