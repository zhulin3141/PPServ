#!/usr/bin/env python
# coding:utf-8

from common import *
from base_module import BaseModule
from lang import *
import wx
import os
import _winreg

class Mod_Memcached(BaseModule):
    '''Memcached模块类'''
    def __init__(self, name):
        BaseModule.__init__(self, name)
        self.reg_base_path = ''
        self.params_list = []

        self.parse_config()

        self.cfg_ctr = {}

    def parse_config(self):
        try:
            config_data = _winreg.QueryValueEx(self.get_service_key(), 'ImagePath')[0].split('-')
        except:
            print Lang().get('error_install_data') % self.service_name

        #可用的配置项
        self.usable_cfg_item = ['p','l','u','m','M','c','f','n']
        self.reg_base_path = config_data[0].strip() + " -d runservice"
        self.params_list = [config_item.strip().split(' ') for config_item in config_data[1:] if config_item.strip()[0] !='d']

    def save_config(self, event):
        content = self.reg_base_path
        config_str = ' '

        for param_name in self.usable_cfg_item:
            val = self.cfg_ctr[param_name].GetValue()
            if val:
                config_str += "-%s %s " % (param_name, val)

        _winreg.SetValueEx(self.get_service_key(), "ImagePath", 0, _winreg.REG_SZ, content + config_str)

    def get_service_key(self):
        """获取当前服务对应的key"""
        service_key_str = r'SYSTEM\CurrentControlSet\Services\%s' % self.service_name

        try:
            service_key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, service_key_str, 0, KEY_ALL_ACCESS)
        except:
            service_key = _winreg.CreateKey(_winreg.HKEY_LOCAL_MACHINE, service_key_str)
        return service_key

    def install_service(self):
        '''安装服务后根据配置中的数据修改memcached服务的数据'''
        result = super(Mod_Memcached, self).install_service()
        execute("sc description %s \"%s\"" % (self.service_name, self.service_name))
        return result

    def set_advt_frame(self, parent):
        self.setting_panel = wx.Panel(parent)
        self.setting_panel.SetSizer(self.setting_sizer)
        parent.AddPage(self.setting_panel, self.module_name)

        self.opt_sizer = wx.BoxSizer(wx.VERTICAL)
        self.grid_sizer = wx.FlexGridSizer(rows=15, cols=6)

        #添加所有的可用配置的文本框
        for param_name in self.usable_cfg_item:
            lbl = wx.StaticText(self.setting_panel, -1, Lang().get('mem_param_' + param_name))
            self.cfg_ctr[param_name] = txt = wx.TextCtrl(self.setting_panel, -1)

            self.grid_sizer.Add(lbl, 0, wx.ALL, 5)
            self.grid_sizer.Add(txt, 0, wx.ALL, 3)

        #设置已经有配置的文本框
        for param_name, param_val in self.params_list:
            self.cfg_ctr[param_name].SetValue(param_val)

        consoleBtn = wx.Button(self.setting_panel, -1, Lang().get('console'))
        consoleBtn.Bind(wx.EVT_BUTTON, self.open_console)

        save_btn = wx.Button(self.setting_panel, -1, Lang().get('mem_save_config'))
        save_btn.Bind(wx.EVT_BUTTON, self.save_config)

        self.handler_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.handler_sizer.AddMany([
            (consoleBtn),
            (save_btn)
        ])

        self.opt_sizer.Add(self.grid_sizer)
        self.opt_sizer.Add(self.handler_sizer, 0, wx.TOP, 5)
        self.setting_sizer.Add(self.opt_sizer, 0, wx.ALL, 5)

    def open_console(self, event):
        open_cmd(self.path)
