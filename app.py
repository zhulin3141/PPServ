#!/usr/bin/env python
# coding:utf-8

import wx
import module
from lang import *

VERSION = '1.1'
APPNAME = 'PPServ'

class App(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, None, -1, APPNAME + VERSION, size=(1000, 500))
        self.SetBackgroundColour('white')
        self.Center()
        self.Show()

        sizer = wx.BoxSizer(wx.VERTICAL)

        topSizer = wx.BoxSizer(wx.HORIZONTAL)
        modSizer = wx.FlexGridSizer(rows=5, cols=2)

        runBox = wx.StaticBox(self, -1, Lang().get('autorun_label'), name="run_box")
        runSizer = wx.StaticBoxSizer(runBox, wx.HORIZONTAL)

        for module_name, mod in module.loadModules.items():
            run = wx.CheckBox(self, -1, module_name, size=[120,13])
            state = wx.StaticText(self, -1, "stop")
            modSizer.Add(run, 0, wx.ALL, 5)
            modSizer.Add(state, 0, wx.ALL, 5)

        startAllBtn = wx.Button(self, -1, Lang().get('start_all_service'), size=(120,70))
        stopAllBtn = wx.Button(self, -1, Lang().get('stop_all_service'), size=(120,70))

        runSizer.Add(modSizer, 0, wx.LEFT | wx.RIGHT, 5)
        runSizer.Add(startAllBtn, 0, wx.TOP | wx.BOTTOM | wx.LEFT, 20)
        runSizer.Add(stopAllBtn, 0, wx.ALL, 20)
        topSizer.Add(runSizer, 0, wx.ALL, 10)


        oftenBox = wx.StaticBox(self, -1, Lang().get('often_label'), name="often_box")
        oftenSizer = wx.StaticBoxSizer(oftenBox, wx.VERTICAL)

        editHostBtn = wx.Button(self, -1, Lang().get('edit_hosts'), size=(110,25))
        startupBtn = wx.Button(self, -1, Lang().get('addto_startup'), size=(110,25))
        oftenSizer.Add(editHostBtn, 0, wx.ALL, 5)
        oftenSizer.Add(startupBtn, 0, wx.ALL, 5)

        topSizer.Add(oftenSizer, 0, wx.ALL, 10)

        stateSizer = wx.BoxSizer(wx.VERTICAL)
        stateBox = wx.TextCtrl(self, -1, "", size=[600, 100], style=wx.TE_MULTILINE)
        stateSizer.Add(stateBox, 0, wx.EXPAND | wx.ALL, 10)

        sizer.Add(topSizer, 0)
        sizer.Add(stateSizer, 0, wx.EXPAND)

        self.SetSizer(sizer)
        self.Fit()


if __name__ == '__main__':
    app = wx.App()
    App().Show()
    app.MainLoop()
