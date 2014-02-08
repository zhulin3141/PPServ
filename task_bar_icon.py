#!/usr/bin/env python
# coding:utf-8

import wx
from lang import *
from common import *

class TaskBarIcon(wx.TaskBarIcon):
    ID_MainPage = wx.NewId()
    ID_About = wx.NewId()
    ID_Minshow = wx.NewId()
    ID_Closeshow = wx.NewId()

    def __init__(self, frame):
        wx.TaskBarIcon.__init__(self)
        self.frame = frame
        self.set_taskbar_icon()
        self.Bind(wx.EVT_TASKBAR_LEFT_DCLICK, self.on_taskbar_left_dclick)
        self.Bind(wx.EVT_MENU, open_main_page, id=self.ID_MainPage)
        self.Bind(wx.EVT_MENU, self.frame.About, id=self.ID_About)
        self.Bind(wx.EVT_MENU, self.frame.OnHide, id=self.ID_Minshow)
        self.Bind(wx.EVT_MENU, self.frame.OnClose, id=self.ID_Closeshow)

    def on_taskbar_left_dclick(self, event):
        if self.frame.IsIconized():
           self.frame.Iconize(False)
        if not self.frame.IsShown():
           self.frame.Show(True)
        self.frame.Raise()

    def CreatePopupMenu(self):
        menu = wx.Menu()
        menu.Append(self.ID_MainPage, Lang().get('main_page'))
        menu.Append(self.ID_Minshow, Lang().get('hide_form'))
        menu.Append(self.ID_About, Lang().get('menu_about'))
        menu.Append(self.ID_Closeshow, Lang().get('menu_quit'))
        return menu

    def set_taskbar_icon(self, size=(32, 32)):
        icon = wx.Icon(name='icon.ico', type=wx.BITMAP_TYPE_ICO, desiredWidth=size[0], desiredHeight=size[1])
        self.SetIcon(icon, APPNAME)
