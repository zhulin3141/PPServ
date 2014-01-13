#!/usr/bin/env python
# coding:utf-8

from common import *
from base_module import BaseModule
import re
import wx

class Mod_Apache(BaseModule):
    '''Apache模块类'''
    def __init__(self, name):
        BaseModule.__init__(self, name)
        self.conf_file = BASE_DIR + self.path + "\conf\httpd.conf"

    def set_advt_frame(self, parent):
        apachePanel = wx.Panel(parent.advtTab)
        parent.advtTab.AddPage(apachePanel, self.module_name)

        content = open(self.conf_file,'r').read()
        loadModuleData = re.findall('(^#*)LoadModule (.+_module)', content, re.M)
        self.moduleList = [modName for (isLoaded, modName) in loadModuleData]
        self.moduleLoad = [isLoaded.strip() == '' for (isLoaded, modName) in loadModuleData]

        self.loadList = wx.CheckListBox(apachePanel, -1, size=wx.DefaultSize, choices=self.moduleList)
        self.loadList.Bind(wx.EVT_CHECKLISTBOX, self.change_module_state)

        for i, isLoad in enumerate(self.moduleLoad):
            self.loadList.Check(i, isLoad)

        wx.TextCtrl(apachePanel, -1, self.get_default_port())
        wx.TextCtrl(apachePanel, -1, self.get_doc_root())
        sizer = wx.BoxSizer(wx.VERTICAL)

    def change_module_state(self, event):
        index = event.GetInt()
        moduleName = self.moduleList[index]
        if self.loadList.IsChecked(index):
            #如果选中则替换掉#，即加载该模块
            self.replace(self.conf_file, r'#+LoadModule ' + moduleName, 'LoadModule ' + moduleName)
        else:
            self.replace(self.conf_file, r'LoadModule ' + moduleName, '#LoadModule ' + moduleName)

    def get_default_port(self):
        return "80"

    def get_doc_root(self):
        return "d:/wamp/www/"
