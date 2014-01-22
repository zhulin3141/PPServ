#!/usr/bin/env python
# coding:utf-8

import wx
from common import *
from conf import Conf
from module.module_factory import ModuleFactory
from wx.lib.stattext import GenStaticText
import webbrowser

class StateLabel(GenStaticText):
    """
    根据状态显示不同的颜色显示
    """

    def __init__(self, parent, id=-1, label='', pos=(-1, -1),
        size=(-1, -1), style=0, name=''):

        GenStaticText.__init__(self, parent, id, label, pos, size, style, name)

        self.state_config = Conf().get('state_style')
        font = 'Verdana'
        self.normal_font = wx.Font(9, wx.SWISS, wx.NORMAL, wx.BOLD, False, font)
        self.underline_font = wx.Font(9, wx.SWISS, wx.NORMAL, wx.BOLD, True, font)

        self.SetFont(self.normal_font)
        self.SetForegroundColour('red')
        self.SetBackgroundColour('white')

        self.Bind(wx.EVT_MOUSE_EVENTS, self.on_mouse_event)
        self.Bind(wx.EVT_MOTION, self.on_mouse_event)

    def on_mouse_event(self, event):
        if event.Moving():
            self.SetCursor(wx.StockCursor(wx.CURSOR_HAND))
            self.SetFont(self.underline_font)
        elif event.LeftUp():
            mod = ModuleFactory.factory(self.name)
            state = mod.get_state().upper()
            if state == RUNNING:
                mod.stop_service()
            elif state == STOPPED:
                mod.start_service()
        else:
            self.SetCursor(wx.NullCursor)
            self.SetFont(self.normal_font)
        event.Skip()

    def set_label(self, label):
        super(StateLabel, self).SetLabel(label)
        label = label.upper()
        state_style = self.state_config[label]

        if label in [RUNNING,STOPPED,UNKNOWN]:
            if 'background' in state_style:
                self.SetBackgroundColour(state_style['background'])
            if 'foreground' in state_style:
                self.SetForegroundColour(state_style['foreground'])
