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
        self.SetIcon(wx.Icon(name='icon.ico', type=wx.BITMAP_TYPE_ICO), APPNAME)
        self.Bind(wx.EVT_TASKBAR_LEFT_DCLICK, self.OnTaskBarLeftDClick)
        self.Bind(wx.EVT_MENU, open_main_page, id=self.ID_MainPage)
        self.Bind(wx.EVT_MENU, self.OnAbout, id=self.ID_About)
        self.Bind(wx.EVT_MENU, self.OnMinshow, id=self.ID_Minshow)
        self.Bind(wx.EVT_MENU, self.OnCloseshow, id=self.ID_Closeshow)

    def OnTaskBarLeftDClick(self, event):
        if self.frame.IsIconized():
           self.frame.Iconize(False)
        if not self.frame.IsShown():
           self.frame.Show(True)
        self.frame.Raise()

    def OnAbout(self, event):
        wx.MessageBox(APPNAME, Lang().get('about_title'))

    def OnMinshow(self, event):
        self.frame.OnHide(event)

    def OnCloseshow(self, event):
        self.frame.OnClose(event)

    def CreatePopupMenu(self):
        menu = wx.Menu()
        menu.Append(self.ID_MainPage, Lang().get('main_page'))
        menu.Append(self.ID_Minshow, Lang().get('hide_form'))
        menu.Append(self.ID_About, Lang().get('menu_about'))
        menu.Append(self.ID_Closeshow, Lang().get('menu_quit'))
        return menu
