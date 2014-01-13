#!/usr/bin/env python
# coding:utf-8

import wx
import logging
import logging.config
import module
from module.module_factory import *
from conf import *
from lang import *
from cache import *
from common import *
from message_handler import *
import state_label
import task_bar_icon
from wx.lib.pubsub import pub


class Ui(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, None, -1, APPNAME + VERSION, size=(800, 230))
        self.SetIcon(wx.Icon('icon.ico', wx.BITMAP_TYPE_ICO))
        self.taskBarIcon = task_bar_icon.TaskBarIcon(self)
        self.Bind(wx.EVT_CLOSE, self.OnHide)
        self.Bind(wx.EVT_ICONIZE, self.OnIconfiy)
        self.SetBackgroundColour('white')
        self.InitUi()

    def InitUi(self):
        self.data = Cache().get()
        self.lbl = {}

        self.basicPanel = wx.Panel(self, size=self.GetSize())
        self.advtPanel = wx.Panel(self, size=self.GetSize())
        self.advtPanel.Hide()

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.basicSizer = wx.BoxSizer(wx.VERTICAL)
        self.advtSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.basicPanel.SetSizer(self.basicSizer)
        self.advtPanel.SetSizer(self.advtSizer)

        self.runBox = wx.StaticBox(self.basicPanel, -1, Lang().get('autorun_label'), name="run_box")

        self.CreateModuleList()
        startAllBtn = wx.Button(self.basicPanel, -1, Lang().get('start_all_service'), size=(120, 70), name='start')
        stopAllBtn = wx.Button(self.basicPanel, -1, Lang().get('stop_all_service'), size=(120, 70), name='stop')
        startAllBtn.Bind(wx.EVT_BUTTON, self.BatchHandlerServices)
        stopAllBtn.Bind(wx.EVT_BUTTON, self.BatchHandlerServices)

        runSizer = wx.StaticBoxSizer(self.runBox, wx.HORIZONTAL)
        runSizer.Add(self.modSizer, 0, wx.LEFT | wx.RIGHT, 5)
        runSizer.Add(startAllBtn, 0, wx.ALL, 10)
        runSizer.Add(stopAllBtn, 0, wx.ALL, 10)

        self.CreateOften()
        topSizer = wx.BoxSizer(wx.HORIZONTAL)
        topSizer.Add(runSizer, 0, wx.ALL)
        topSizer.Add(self.oftenSizer, 0, wx.LEFT, 10)
        self.basicSizer.Add(topSizer)

        self.stateBox = wx.TextCtrl(self.basicPanel, -1, "", size=(600, 100), style=wx.TE_MULTILINE)
        self.basicSizer.Add(self.stateBox, 0, wx.EXPAND | wx.TOP, 5)

        self.advtTab = wx.Notebook(self.advtPanel)
        self.advtSizer.Add(self.advtTab, -1, wx.EXPAND | wx.RIGHT, 5)
        for mod in ModuleFactory.get_module_list():
            mod.set_advt_frame(self)

        oftenBtnSize = (110, 25)
        self.advtBox = wx.StaticBox(self.advtPanel, -1, Lang().get('often_label'))
        self.advtOftenSizer = wx.StaticBoxSizer(self.advtBox, wx.VERTICAL)
        basicBtn = wx.Button(self.advtPanel, -1, Lang().get('basic_setting'), size=oftenBtnSize, name='basic')
        basicBtn.Bind(wx.EVT_BUTTON, self.Toggle)
        self.advtOftenSizer.Add(basicBtn, 1, wx.EXPAND | wx.ALL, 5)
        self.advtSizer.Add(self.advtOftenSizer, 0, wx.RIGHT, 5)

        self.sizer.Add(self.basicPanel, 1, wx.EXPAND | wx.ALL, 10)
        self.sizer.Add(self.advtPanel, 1, wx.EXPAND | wx.ALL, 10)

        self.SetSizerAndFit(self.sizer)

    def CreateOften(self):
        oftenBox = wx.StaticBox(self.basicPanel, -1, Lang().get('often_label'), name="often_box")
        self.oftenSizer = wx.StaticBoxSizer(oftenBox, wx.VERTICAL)

        oftenData = (('edit_hosts', open_hosts),
                     ('addto_startup', set_autorun),
                     ('advt_setting', self.Toggle))

        oftenBtnSize = (110, 25)

        for label, handler in oftenData:
            oftenBtn = wx.Button(self.basicPanel, -1, Lang().get(label), size=oftenBtnSize, name=label)
            oftenBtn.Bind(wx.EVT_BUTTON, handler)
            self.oftenSizer.Add(oftenBtn, 0, wx.ALL, 5)

    def CreateModuleList(self):
        self.modSizer = wx.FlexGridSizer(rows=5, cols=2)
        for module_name, mod in BaseModule.list_module_data().items():
            run = wx.CheckBox(self.basicPanel, -1, module_name, size=[120, 13])
            run.SetValue(run.Label in self.data['autorun'] and self.data['autorun'][run.Label])
            run.Bind(wx.EVT_CHECKBOX, self.SaveSelect)

            self.lbl[module_name] = state_label.StateLabel(self.basicPanel, -1, "stop", size=(50, 15), mappingData=module_name)
            self.modSizer.Add(run, 0, wx.ALL, 5)
            self.modSizer.Add(self.lbl[module_name], 0, wx.ALL, 5)


    def OnHide(self):
        """隐藏"""
        self.Hide()

    def OnIconfiy(self, event):
        """点击关闭时只退出监控界面"""
        self.Hide()
        event.Skip()

    def OnClose(self, event):
        """退出"""
        self.taskBarIcon.Destroy()
        self.Destroy()

    def SaveSelect(self, event):
        """保存选中的自动运行的程序的状态"""
        pub.sendMessage('SaveSelect',event=event)

    def BatchHandlerServices(self, event):
        """批量处理各模块启动或停止服务"""
        pub.sendMessage('BatchHandlerServices',event=event)

    def Toggle(self, event):
        #保持Panel和Frame的大小一致
        self.basicPanel.SetSize(self.GetSize())
        self.advtPanel.SetSize(self.GetSize())
        if event.GetEventObject().GetName() == 'basic':
            self.basicPanel.Show()
            self.advtPanel.Hide()
        else:
            self.basicPanel.Hide()
            self.advtPanel.Show()