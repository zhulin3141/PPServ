#!/usr/bin/env python
# coding:utf-8

from common import *
from base_module import BaseModule
import wx
import ConfigParser

class Mod_Php(BaseModule):
    '''PHP模块类'''
    def __init__(self, name):
        BaseModule.__init__(self, name)
        self.setting_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.conf_file = BASE_DIR + self.path + "\php.ini"
        self.parse_config_file()

    def parse_config_file(self):
        self.content = open(self.conf_file,'r').read()

    def set_advt_frame(self, parent):
        self.setting_panel = wx.Panel(parent)
        self.setting_panel.SetSizer(self.setting_sizer)
        parent.AddPage(self.setting_panel, self.module_name)

        self.set_load_module()

        cfg = ConfigParser.SafeConfigParser()
        cfg.read(self.conf_file)
        all_items = [item[0] for item in cfg.items('PHP')]
        options = ['short_open_tag', 'asp_tags', 'max_execution_time', 'memory_limit', 'error_reporting', 'display_errors']

        #只获取有值的项，即没有；注释的项
        exists_options = list(set(all_items).intersection(set(options)))
        self.grid_sizer = wx.FlexGridSizer(rows=15, cols=2)
        for opt in exists_options:
            lbl = wx.StaticText(self.setting_panel, -1, opt)
            txt = wx.TextCtrl(self.setting_panel, -1, cfg.get('PHP', opt))
            self.grid_sizer.Add(lbl, 0, wx.ALL, 5)
            self.grid_sizer.Add(txt, 0, wx.ALL, 3)

        self.setting_sizer.Add(self.grid_sizer, 0, wx.ALL, 5)

    def change_module_state(self, event):
        index = event.GetInt()
        moduleName = self.moduleList[index]

        if self.loadList.IsChecked(index):
            self.replace(self.conf_file, r';+extension=' + moduleName, 'extension=' + moduleName)
        else:
            self.replace(self.conf_file, r'extension=' + moduleName, ';extension=' + moduleName)

    def set_load_module(self):
        loadModuleData = re.findall('(^;*)extension=(php_.*).dll', self.content, re.M)
        self.moduleList = [modName for (isLoaded, modName) in loadModuleData]
        self.moduleLoad = [isLoaded.strip() == '' for (isLoaded, modName) in loadModuleData]

        self.loadList = wx.CheckListBox(self.setting_panel, -1, size=wx.DefaultSize, choices=self.moduleList)
        self.loadList.Bind(wx.EVT_CHECKLISTBOX, self.change_module_state)

        for i, isLoad in enumerate(self.moduleLoad):
            self.loadList.Check(i, isLoad)

        self.setting_sizer.Add(self.loadList, 0, wx.EXPAND)
