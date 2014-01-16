#!/usr/bin/env python
# coding:utf-8

from common import *
from base_module import BaseModule
import wx
import ConfigParser
from lang import Lang

class Mod_Php(BaseModule):
    '''PHP模块类'''
    def __init__(self, name):
        BaseModule.__init__(self, name)
        self.conf_file = BASE_DIR + self.path + "\php.ini"
        self.parse_config_file()

        self.cfg_ctr = {}

    def parse_config_file(self):
        self.content = open(self.conf_file,'r').read()
        self.cfg = ConfigParser.SafeConfigParser()

        self.cfg.read(self.conf_file)
        all_items = [item[0] for item in self.cfg.items('PHP')]
        options = ['short_open_tag', 'asp_tags', 'max_execution_time', 'memory_limit', 'error_reporting', 'display_errors']

        #只获取有值的项，即没有；注释的项
        self.exists_options = list(set(all_items).intersection(set(options)))

    def set_advt_frame(self, parent):
        self.setting_panel = wx.Panel(parent)
        self.setting_panel.SetSizer(self.setting_sizer)
        parent.AddPage(self.setting_panel, self.module_name)

        self.set_load_module()
        self.opt_sizer = wx.BoxSizer(wx.VERTICAL)
        self.grid_sizer = wx.FlexGridSizer(rows=15, cols=2)
        for opt in self.exists_options:
            lbl = wx.StaticText(self.setting_panel, -1, opt)
            self.cfg_ctr[opt] = txt = wx.TextCtrl(self.setting_panel, -1, self.cfg.get('PHP', opt))
            self.grid_sizer.Add(lbl, 0, wx.ALL, 5)
            self.grid_sizer.Add(txt, 0, wx.ALL, 3)

        conf_btn = wx.Button(self.setting_panel, -1, Lang().get('php_config_file'))
        conf_btn.Bind(wx.EVT_BUTTON, self.open_config_file)

        save_btn = wx.Button(self.setting_panel, -1, Lang().get('php_save_config'))
        save_btn.Bind(wx.EVT_BUTTON, self.save_config)

        self.handler_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.handler_sizer.AddMany([
            (conf_btn),
            (save_btn)
        ])

        self.opt_sizer.Add(self.grid_sizer)
        self.opt_sizer.Add(self.handler_sizer, 0, wx.TOP, 5)
        self.setting_sizer.Add(self.opt_sizer, 0, wx.ALL, 5)

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

    def open_config_file(self, event):
        open_file(self.conf_file)

    def save_config(self, event):
        #保存配置
        for opt in self.exists_options:
            print opt
            self.cfg.set('PHP', opt, self.cfg_ctr[opt].GetValue())
            fp = open(self.conf_file,'w')
            self.cfg.write(fp)
            fp.close()

        self.parse_config_file()
