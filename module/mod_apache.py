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
        self.setting_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.conf_file = BASE_DIR + self.path + "\conf\httpd.conf"
        self.parse_config_file()

    def parse_config_file(self):
        self.content = open(self.conf_file,'r').read()
        self.listen_ports = re.findall('^Listen +([0-9]+)', self.content, re.M)
        self.doc_root = re.findall('^DocumentRoot +(.+)', self.content, re.M)

    def set_advt_frame(self, parent):
        self.setting_panel = wx.Panel(parent)
        self.setting_panel.SetSizer(self.setting_sizer)
        parent.AddPage(self.setting_panel, self.module_name)

        self.set_load_module()

        port = wx.TextCtrl(self.setting_panel, -1, self.get_default_port())
        doc_root = wx.TextCtrl(self.setting_panel, -1, self.get_doc_root())
        self.setting_sizer.Add(port)
        self.setting_sizer.Add(doc_root)

    def change_module_state(self, event):
        index = event.GetInt()
        moduleName = self.moduleList[index]
        if self.loadList.IsChecked(index):
            #如果选中则替换掉#，即加载该模块
            self.replace(self.conf_file, r'#+LoadModule ' + moduleName, 'LoadModule ' + moduleName)
        else:
            self.replace(self.conf_file, r'LoadModule ' + moduleName, '#LoadModule ' + moduleName)

    def set_load_module(self):
        loadModuleData = re.findall('(^#*)LoadModule (.+_module)', self.content, re.M)
        self.moduleList = [modName for (isLoaded, modName) in loadModuleData]
        self.moduleLoad = [isLoaded.strip() == '' for (isLoaded, modName) in loadModuleData]

        self.loadList = wx.CheckListBox(self.setting_panel, -1, size=wx.DefaultSize, choices=self.moduleList)
        self.loadList.Bind(wx.EVT_CHECKLISTBOX, self.change_module_state)

        for i, isLoad in enumerate(self.moduleLoad):
            self.loadList.Check(i, isLoad)

        self.setting_sizer.Add(self.loadList)

    def get_default_port(self):
        return self.listen_ports[0]

    def get_doc_root(self):
        return self.doc_root[0].strip("\"' ")
