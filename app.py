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
from ui import *
from wx.lib.pubsub import pub


class App(wx.Frame):

    def __init__(self):
        self.ui = Ui()
        self.ui.Center()

        pub.subscribe(self.BatchHandlerServices, 'BatchHandlerServices')
        pub.subscribe(self.SaveSelect, 'SaveSelect')
        self.ui.Show()
        self.Start()

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
        for module_name, mod_data in BaseModule.list_module_data().items():
            mod = ModuleFactory.factory(module_name)
            if mod.is_install():
                self.ui.lbl[module_name].SetLabel(mod.get_state().lower())
            else:
                mod.install_service()
        wx.CallLater(3000, self.UpdateState)

    def SetLog(self):
        #从配置文件中设置log
        logging.config.dictConfig(Conf().get('logging'))

        handler = MessageHandler(self.ui.stateBox)
        log = logging.getLogger()
        log.addHandler(handler)
        log.setLevel(logging.INFO)

    def BatchHandlerServices(self, event):
        """批量处理各模块启动或停止服务"""
        for module_name, state in Cache().get("autorun").items():
            if state:
                mod = ModuleFactory.factory(module_name)
                if event.GetEventObject().GetName() == "start":
                    wx.CallAfter(mod.start_service)
                else:
                    wx.CallAfter(mod.stop_service)



app = wx.App()
frame = App()
app.MainLoop()
