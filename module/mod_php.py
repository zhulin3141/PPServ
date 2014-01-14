#!/usr/bin/env python
# coding:utf-8

from common import *
from base_module import BaseModule
import wx

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
