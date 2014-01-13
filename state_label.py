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
        size=(-1, -1), style=0, name='', mappingData=None):

        GenStaticText.__init__(self, parent, id, label, pos, size, style, name)

        self.normalFont = wx.Font(9, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Verdana')
        self.underLineFont = wx.Font(9, wx.SWISS, wx.NORMAL, wx.BOLD, True, 'Verdana')

        self.SetFont(self.normalFont)
        self.SetForegroundColour('red')
        self.SetBackgroundColour('white')

        self.module = mappingData

        self.Bind(wx.EVT_MOUSE_EVENTS, self.OnMouseEvent)
        self.Bind(wx.EVT_MOTION, self.OnMouseEvent)

    def OnMouseEvent(self, event):
        if event.Moving():
            self.SetCursor(wx.StockCursor(wx.CURSOR_HAND))
            self.SetFont(self.underLineFont)
        elif event.LeftUp():
            mod = ModuleFactory.factory(self.module)
            state = mod.get_state().upper()
            if state == RUNNING:
                mod.stop_service()
            elif state == STOPPED:
                mod.start_service()
        else:
            self.SetCursor(wx.NullCursor)
            self.SetFont(self.normalFont)
        event.Skip()

    def SetLabel(self, label):
        super(StateLabel, self).SetLabel(label)
        label = label.upper()
        stateConfig = Conf().get('state_style')[label]

        if label in [RUNNING,STOPPED,UNKNOWN]:
            if 'background' in stateConfig:
                self.SetBackgroundColour(stateConfig['background'])
            if 'foreground' in stateConfig:
                self.SetForegroundColour(stateConfig['foreground'])
