#!/usr/bin/env python
# coding:utf-8

from common import *
from base_module import BaseModule
import re
import wx
import os
from lang import Lang

class Mod_Apache(BaseModule):
    '''Apache模块类'''
    def __init__(self, name):
        BaseModule.__init__(self, name)
        self.conf_file = BASE_DIR + self.path + "\conf\httpd.conf"
        self.parse_config_file()

    def parse_config_file(self):
        self.content = open(self.conf_file,'r').read()
        self.listen_ports = re.findall('^Listen +([0-9]+)', self.content, re.M)
        self.doc_root = re.findall('^DocumentRoot +(.+)', self.content, re.M)
        self.error_log_file = re.findall('^ErrorLog +(.+)', self.content, re.M)

    def set_advt_frame(self, parent):
        self.setting_panel = wx.Panel(parent)
        self.setting_panel.SetSizer(self.setting_sizer)
        parent.AddPage(self.setting_panel, self.module_name)

        self.set_load_module()

        lbl_port = wx.StaticText(self.setting_panel, -1, Lang().get('apache_port'))
        self.cfg_port = wx.TextCtrl(self.setting_panel, -1, self.get_default_port(), size=(200, 20))
        lbl_doc_root = wx.StaticText(self.setting_panel, -1, Lang().get('apache_doc_root'))
        self.cfg_doc_root = wx.TextCtrl(self.setting_panel, -1, self.get_doc_root(), size=(200, 20))

        select_dir_btn = wx.Button(self.setting_panel, -1, Lang().get('apache_choose_doc_root'))
        select_dir_btn.Bind(wx.EVT_BUTTON, self.choose_dir)

        conf_btn = wx.Button(self.setting_panel, -1, Lang().get('apache_config_file'))
        conf_btn.Bind(wx.EVT_BUTTON, self.open_config_file)
        log_btn = wx.Button(self.setting_panel, -1, Lang().get('apache_log_file'))
        log_btn.Bind(wx.EVT_BUTTON, self.open_log_file)

        save_btn = wx.Button(self.setting_panel, -1, Lang().get('apache_save_config'))
        save_btn.Bind(wx.EVT_BUTTON, self.save_config)

        self.opt_sizer = wx.BoxSizer(wx.VERTICAL)
        self.grid_sizer = wx.FlexGridSizer(rows=5, cols=3)
        self.grid_sizer.AddMany([
            (lbl_port, 0, wx.ALL, 5),
            (self.cfg_port, 0, wx.ALL, 5),
            (wx.StaticText(self.setting_panel)),
            (lbl_doc_root, 0, wx.ALL, 5),
            (self.cfg_doc_root, 0, wx.ALL, 5),
            (select_dir_btn)
        ])

        self.handler_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.handler_sizer.AddMany([
            (conf_btn),
            (log_btn),
            (save_btn)
        ])

        self.opt_sizer.Add(self.grid_sizer)
        self.opt_sizer.Add(self.handler_sizer, 0, wx.TOP, 5)
        self.setting_sizer.Add(self.opt_sizer, 0, wx.ALL, 5)

    def change_module_state(self, event):
        index = event.GetInt()
        module_name = self.module_list[index]
        if self.load_list.IsChecked(index):
            #如果选中则替换掉#，即加载该模块
            self.replace(self.conf_file, r'#+LoadModule ' + module_name, 'LoadModule ' + module_name)
        else:
            self.replace(self.conf_file, r'LoadModule ' + module_name, '#LoadModule ' + module_name)

    def set_load_module(self):
        load_module_data = re.findall('(^#*)LoadModule (.+_module)', self.content, re.M)
        self.module_list = [mod_name for (is_loaded, mod_name) in load_module_data]
        self.module_load = [is_loaded.strip() == '' for (is_loaded, mod_name) in load_module_data]

        self.load_list = wx.CheckListBox(self.setting_panel, -1, choices=self.module_list)
        self.load_list.Bind(wx.EVT_CHECKLISTBOX, self.change_module_state)

        for i, isLoad in enumerate(self.module_load):
            self.load_list.Check(i, isLoad)

        self.setting_sizer.Add(self.load_list, 0, wx.EXPAND)

    def get_default_port(self):
        return self.listen_ports[0]

    def get_doc_root(self):
        return self.doc_root[0].strip("\"' ")

    def open_log_file(self, event):
        open_file(self.error_log_file)

    def open_config_file(self, event):
        open_file(self.conf_file)

    def save_config(self, event):
        #保存配置
        self.replace(self.conf_file, r'^Listen +([0-9]+)', 'Listen ' + self.cfg_port.GetValue(), 1)
        self.replace(self.conf_file, r'^DocumentRoot +(.+)', 'DocumentRoot ' + self.cfg_doc_root.GetValue())
        self.replace(self.conf_file, r'^<Directory "%s">' % self.doc_root[0].replace('\\','\\\\'),
            '<Directory "%s">' % self.cfg_doc_root.GetValue(), 1)
        self.parse_config_file()

    def choose_dir(self, event):
        #选择并更新根目录
        select_dir = wx.DirDialog(None, Lang().get('apache_choose_doc_root') + ':',
            self.cfg_doc_root.GetLabelText(), style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
        if select_dir.ShowModal() == wx.ID_OK and os.path.isdir(select_dir.GetPath()):
                self.cfg_doc_root.SetLabelText(select_dir.GetPath())
        select_dir.Destroy()
