#!/usr/bin/env python
# coding:utf-8

import wx
import logging
import logging.config
from module.module_factory import *
from conf import *
from lang import *
from cache import *
from common import *
from message_handler import *
import state_label
import task_bar_icon
from plugin_manager import DirectoryPluginManager


class App(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, None, -1, APPNAME + VERSION, size=(800, 230))
        self.SetIcon(wx.Icon('icon.ico', wx.BITMAP_TYPE_ICO))
        self.tray_icon = task_bar_icon.TaskBarIcon(self)
        self.Bind(wx.EVT_CLOSE, self.OnHide)
        self.Bind(wx.EVT_ICONIZE, self.OnIconfiy)
        self.SetBackgroundColour('white')
        self.init_ui()
        self.Center()
        self.Show()

    def init_ui(self):
        self.data = Cache().get()
        self.lbl = {}
        self.btn_size = (110, 25)
        self.mod_list = {}

        for mod in ModuleFactory.get_module_list():
            self.mod_list[mod.module_name] = mod

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.basic_panel = wx.Panel(self, size=self.GetSize())
        self.advt_panel = wx.Panel(self, size=self.GetSize())
        self.advt_panel.Hide()

        self.init_basic_panel()
        self.init_advt_panel()

        self.sizer.Add(self.basic_panel, 1, wx.EXPAND | wx.ALL, 10)
        self.sizer.Add(self.advt_panel, 1, wx.EXPAND | wx.ALL, 0)

        self.SetSizerAndFit(self.sizer)
        self.start()

    def init_basic_panel(self):
        self.basic_sizer = wx.BoxSizer(wx.VERTICAL)
        self.basic_panel.SetSizer(self.basic_sizer)

        self.run_box = wx.StaticBox(self.basic_panel, -1, Lang().get('autorun_label'), name="run_box")
        self.create_module_list()

        run_btn_size = (120, 70)
        start_all_btn = wx.Button(self.basic_panel, -1, Lang().get('start_all_service'), size=run_btn_size, name='start')
        stop_all_btn = wx.Button(self.basic_panel, -1, Lang().get('stop_all_service'), size=run_btn_size, name='stop')
        start_all_btn.Bind(wx.EVT_BUTTON, self.batch_handler_services)
        stop_all_btn.Bind(wx.EVT_BUTTON, self.batch_handler_services)

        run_sizer = wx.StaticBoxSizer(self.run_box, wx.HORIZONTAL)
        run_sizer.AddMany([
            (self.mod_sizer, 0, wx.LEFT | wx.RIGHT, 5),
            (start_all_btn, 0, wx.ALL, 10),
            (stop_all_btn, 0, wx.ALL, 10)
        ])

        self.create_often()
        top_sizer = wx.BoxSizer(wx.HORIZONTAL)
        top_sizer.Add(run_sizer, 0, wx.ALL)
        top_sizer.Add(self.often_sizer, 0, wx.LEFT, 10)
        self.basic_sizer.Add(top_sizer)

        self.state_box = wx.TextCtrl(self.basic_panel, -1, "", size=(600, 100), style=wx.TE_MULTILINE)
        self.bottom_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.bottom_sizer.Add(self.state_box, 1, wx.ALL | wx.EXPAND, 5)
        self.basic_sizer.Add(self.state_box, 1, wx.EXPAND | wx.TOP, 5)

    def init_advt_panel(self):
        self.advt_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.advt_panel.SetSizer(self.advt_sizer)

        self.advt_tab = wx.Notebook(self.advt_panel)
        self.advt_sizer.Add(self.advt_tab, -1, wx.EXPAND | wx.RIGHT, 5)
        for mod_name, mod in self.mod_list.items():
            mod.set_advt_frame(self.advt_tab)

        self.advt_box = wx.StaticBox(self.advt_panel, -1, Lang().get('often_label'))
        self.advt_often_sizer = wx.StaticBoxSizer(self.advt_box, wx.VERTICAL)

        basic_btn = wx.Button(self.advt_panel, -1, Lang().get('basic_setting'), size=self.btn_size, name='basic')
        basic_btn.Bind(wx.EVT_BUTTON, self.toggle)

        cmd_btn = wx.Button(self.advt_panel, -1, Lang().get('open_cmd'), size=self.btn_size)
        cmd_btn.Bind(wx.EVT_BUTTON, self.open_cmd_curr_dir)

        self.advt_often_sizer.AddMany([
            (basic_btn, 1, wx.EXPAND | wx.ALL, 5),
            (cmd_btn, 1, wx.EXPAND | wx.ALL, 5)
        ])
        self.advt_sizer.Add(self.advt_often_sizer, 0, wx.RIGHT, 5)

    def create_often(self):
        often_box = wx.StaticBox(self.basic_panel, -1, Lang().get('often_label'), name="often_box")
        self.often_sizer = wx.StaticBoxSizer(often_box, wx.VERTICAL)
        self.often_btn_sizer = wx.FlexGridSizer(rows=5, cols=2)

        often_data = (('edit_hosts', open_hosts),
                     ('addto_startup', set_autorun),
                     ('advt_setting', self.toggle))

        for label, handler in often_data:
            often_btn = wx.Button(self.basic_panel, -1, Lang().get(label), size=self.btn_size, name=label)
            often_btn.Bind(wx.EVT_BUTTON, handler)
            self.often_btn_sizer.Add(often_btn, 0, wx.ALL, 5)
        self.often_sizer.Add(self.often_btn_sizer)

    def create_module_list(self):
        self.mod_sizer = wx.FlexGridSizer(rows=5, cols=2)
        for module_name in BaseModule.list_service_module():
            run = wx.CheckBox(self.basic_panel, -1, module_name, size=[120, 13])
            run.SetValue(run.Label in self.data['autorun'] and self.data['autorun'][run.Label])
            run.Bind(wx.EVT_CHECKBOX, self.save_select)

            self.lbl[module_name] = state_label.StateLabel(self.basic_panel, -1, "stop", size=(50, 15), name=module_name)
            self.mod_sizer.Add(run, 0, wx.ALL, 5)
            self.mod_sizer.Add(self.lbl[module_name], 0, wx.ALL, 5)

    def OnHide(self, event):
        """隐藏"""
        self.Hide()

    def OnIconfiy(self, event):
        """点击关闭时只退出监控界面"""
        self.Hide()
        event.Skip()

    def OnClose(self, event):
        """退出"""
        self.tray_icon.Destroy()
        self.Destroy()

    def save_select(self, event):
        """保存选中的自动运行的程序的状态"""
        sender = event.GetEventObject()
        self.data['autorun'][sender.Label] = sender.GetValue()
        Cache().set("autorun", self.data['autorun'])

    def start(self):
        self.set_log()
        wx.CallAfter(self.update_state)

        plugin_manager = DirectoryPluginManager()
        plugin_manager.load_plugins()
        plugins = plugin_manager.get_plugins()

        for plugin in plugins:
            plugin.start(None, {'advt_tab':self.advt_tab})

    def update_state(self):
        """自动更新各模块的状态显示"""
        for module_name in BaseModule.list_service_module():
            mod = self.mod_list[module_name]
            if mod.is_install():
                self.lbl[module_name].set_label(mod.get_state().lower())
            else:
                mod.install_service()
        wx.CallLater(3000, self.update_state)

    def set_log(self):
        #从配置文件中设置log
        logging.config.dictConfig(Conf().get('logging'))

        handler = MessageHandler(self.state_box)
        log = logging.getLogger()
        log.addHandler(handler)
        log.setLevel(logging.INFO)

    def batch_handler_services(self, event):
        """批量处理各模块启动或停止服务"""
        for module_name, state in Cache().get("autorun").items():
            if state:
                mod = self.mod_list[module_name]
                if event.GetEventObject().GetName() == "start":
                    wx.CallAfter(mod.start_service)
                else:
                    wx.CallAfter(mod.stop_service)

    def toggle(self, event):
        #保持Panel和Frame的大小一致
        self.basic_panel.SetSize(self.GetSize())
        self.advt_panel.SetSize(self.GetSize())
        if event.GetEventObject().GetName() == 'basic':
            self.basic_panel.Show()
            self.advt_panel.Hide()
        else:
            self.basic_panel.Hide()
            self.advt_panel.Show()

    def open_cmd_curr_dir(self, event):
        tab_name = self.advt_tab.GetPageText(self.advt_tab.GetSelection())
        open_cmd(self.mod_list[tab_name].path)


app = wx.App()
frame = App()
app.MainLoop()
