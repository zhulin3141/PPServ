#!/usr/bin/env python
# coding:utf-8

from common import *
from base_module import BaseModule
import wx

class Mod_Php(BaseModule):
    '''PHP模块类'''
    def __init__(self, name):
        BaseModule.__init__(self, name)
        self.conf_file = BASE_DIR + self.path + "\php.ini"

    def set_advt_frame(self, parent):
        phpPanel = wx.Panel(parent.advtTab)
        parent.advtTab.AddPage(phpPanel, self.module_name)

        content = open(self.conf_file,'r').read()
        loadModuleData = re.findall('(^;*)extension=(php_.*).dll', content, re.M)
        self.moduleList = [modName for (isLoaded, modName) in loadModuleData]
        self.moduleLoad = [isLoaded.strip() == '' for (isLoaded, modName) in loadModuleData]

        self.loadList = wx.CheckListBox(phpPanel, -1, size=wx.DefaultSize, choices=self.moduleList)
        self.loadList.Bind(wx.EVT_CHECKLISTBOX, self.change_module_state)

        for i, isLoad in enumerate(self.moduleLoad):
            self.loadList.Check(i, isLoad)

    def change_module_state(self, event):
        index = event.GetInt()
        moduleName = self.moduleList[index]

        if self.loadList.IsChecked(index):
            self.replace(self.conf_file, r';+extension=' + moduleName, 'extension=' + moduleName)
        else:
            self.replace(self.conf_file, r'extension=' + moduleName, ';extension=' + moduleName)
