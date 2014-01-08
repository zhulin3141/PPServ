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


class App(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, None, -1, APPNAME + VERSION, size=(1000, 500))
        self.SetIcon(wx.Icon('icon.ico', wx.BITMAP_TYPE_ICO))
        self.taskBarIcon = task_bar_icon.TaskBarIcon(self)
        self.Bind(wx.EVT_CLOSE, self.OnHide)
        self.Bind(wx.EVT_ICONIZE, self.OnIconfiy)
        self.SetBackgroundColour('white')
        self.Center()
        self.Show()

        #基本Panel
        self.basicPanel = wx.Panel(self, size=self.GetSize())
        self.basicPanel.SetBackgroundColour('white')
        basicSizer = wx.BoxSizer(wx.VERTICAL)
        self.basicPanel.SetSizer(basicSizer)

        #高级Panel
        self.advtPanel = wx.Panel(self, size=self.GetSize())
        self.advtPanel.SetBackgroundColour('white')
        advtSizer = wx.BoxSizer(wx.VERTICAL)
        self.advtPanel.SetSizer(advtSizer)
        self.advtPanel.Hide()

        self.advtTab = wx.Notebook(self.advtPanel)
        advtSizer.Add(self.advtTab, -1, wx.EXPAND)
        for mod in ModuleFactory.get_module_list():
            mod.set_advt_frame(self)

        self.data = Cache().get()


        topSizer = wx.BoxSizer(wx.HORIZONTAL)
        modSizer = wx.FlexGridSizer(rows=5, cols=2)

        runBox = wx.StaticBox(self.basicPanel, -1, Lang().get('autorun_label'), name="run_box")

        self.lbl = {}
        for module_name, mod in module.loadModules.items():
            run = wx.CheckBox(self.basicPanel, -1, module_name, size=[120, 13])
            if run.Label in self.data['autorun'] and self.data['autorun'][run.Label] is True:
                run.SetValue(True)
            else:
                run.SetValue(False)
            run.Bind(wx.EVT_CHECKBOX, self.SaveSelect)

            self.lbl[module_name] = state = state_label.StateLabel(self.basicPanel, -1, "stop", size=(50, 15), mappingData=module_name)
            modSizer.Add(run, 0, wx.ALL, 5)
            modSizer.Add(state, 0, wx.ALL, 5)

        startAllBtn = wx.Button(self.basicPanel, -1, Lang().get('start_all_service'), size=(120,70), name='start')
        stopAllBtn = wx.Button(self.basicPanel, -1, Lang().get('stop_all_service'), size=(120,70), name='stop')

        startAllBtn.Bind(wx.EVT_BUTTON, self.BatchHandlerServices)
        stopAllBtn.Bind(wx.EVT_BUTTON, self.BatchHandlerServices)

        runSizer = wx.StaticBoxSizer(runBox, wx.HORIZONTAL)
        runSizer.Add(modSizer, 0, wx.LEFT | wx.RIGHT, 5)
        runSizer.Add(startAllBtn, 0, wx.TOP | wx.BOTTOM | wx.LEFT, 20)
        runSizer.Add(stopAllBtn, 0, wx.ALL, 20)
        topSizer.Add(runSizer, 0, wx.ALL, 10)


        oftenBox = wx.StaticBox(self.basicPanel, -1, Lang().get('often_label'), name="often_box")

        editHostBtn = wx.Button(self.basicPanel, -1, Lang().get('edit_hosts'), size=(110,25))
        editHostBtn.Bind(wx.EVT_BUTTON, open_hosts)
        startupBtn = wx.Button(self.basicPanel, -1, Lang().get('addto_startup'), size=(110,25))
        startupBtn.Bind(wx.EVT_BUTTON, set_autorun)
        advtBtn = wx.Button(self.basicPanel, -1, Lang().get('advt_setting'), size=(110,25), name='advt')
        advtBtn.Bind(wx.EVT_BUTTON, self.Toggle)

        oftenSizer = wx.StaticBoxSizer(oftenBox, wx.VERTICAL)
        oftenSizer.Add(editHostBtn, 0, wx.ALL, 5)
        oftenSizer.Add(startupBtn, 0, wx.ALL, 5)
        oftenSizer.Add(advtBtn, 0, wx.ALL, 5)

        topSizer.Add(oftenSizer, 0, wx.ALL, 10)

        self.stateBox = wx.TextCtrl(self.basicPanel, -1, "", size=[600, 100], style=wx.TE_MULTILINE)
        stateSizer = wx.BoxSizer(wx.VERTICAL)
        stateSizer.Add(self.stateBox, 0, wx.EXPAND | wx.ALL, 10)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(topSizer, 0)
        self.sizer.Add(stateSizer, 0, wx.EXPAND)

        self.SetSizer(self.sizer)
        self.Fit()

        self.Start()

    def OnHide(self, event):
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
        sender = event.GetEventObject()
        self.data['autorun'][sender.Label] = sender.GetValue()
        Cache().set("autorun", self.data['autorun'])

    def Start(self):
        self.SetLog()
        wx.CallAfter(self.UpdateState)

    def UpdateState(self):
        """自动更新各模块的状态显示"""
        for module_name, mod_data in module.loadModules.items():
            mod = ModuleFactory.factory(module_name)
            if mod.is_install():
                self.lbl[module_name].SetLabel(mod.get_state().lower())
            else:
                mod.install_service()
        wx.CallLater(3000, self.UpdateState)

    def SetLog(self):
        #从配置文件中设置log
        logging.config.dictConfig(Conf().get('logging'))

        handler = MessageHandler(self.stateBox)
        log = logging.getLogger()
        log.addHandler(handler)
        log.setLevel(logging.INFO)

    def BatchHandlerServices(self, event):
        """批量处理各模块启动或停止服务"""
        for module_name, state in Cache().get("autorun").items():
            if state is True:
                mod = ModuleFactory.factory(module_name)
                if event.GetEventObject().GetName() == "start":
                    wx.CallAfter(mod.start_service)
                else:
                    wx.CallAfter(mod.stop_service)

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

app = wx.App()
frame = App()
app.MainLoop()
