# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Nov  6 2013)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class Ui
###########################################################################

class Ui ( wx.Frame ):
    
    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"PPServ", pos = wx.DefaultPosition, size = wx.Size( 800,293 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
        
        self.SetSizeHintsSz( wx.Size( -1,-1 ), wx.DefaultSize )
        
        hSizer = wx.BoxSizer( wx.HORIZONTAL )
        
        self.basic_panel = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        self.basic_panel.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
        
        basic_sizer = wx.BoxSizer( wx.VERTICAL )
        
        top_sizer = wx.BoxSizer( wx.HORIZONTAL )
        
        module_sizer = wx.StaticBoxSizer( wx.StaticBox( self.basic_panel, wx.ID_ANY, u"module" ), wx.VERTICAL )
        
        func_sizer = wx.BoxSizer( wx.HORIZONTAL )
        
        self.module_list_sizer = wx.FlexGridSizer( 0, 2, 0, 0 )
        self.module_list_sizer.SetFlexibleDirection( wx.BOTH )
        self.module_list_sizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        
        
        func_sizer.Add( self.module_list_sizer, 1, wx.EXPAND, 5 )
        
        services_sizer = wx.BoxSizer( wx.HORIZONTAL )
        
        self.start_all_service = wx.Button( self.basic_panel, wx.ID_ANY, u"start", wx.DefaultPosition, wx.Size( 120,70 ), 0 )
        services_sizer.Add( self.start_all_service, 0, wx.ALL, 5 )
        
        self.stop_all_service = wx.Button( self.basic_panel, wx.ID_ANY, u"stop", wx.DefaultPosition, wx.Size( 120,70 ), 0 )
        services_sizer.Add( self.stop_all_service, 0, wx.ALL, 5 )
        
        
        func_sizer.Add( services_sizer, 1, wx.EXPAND, 5 )
        
        
        module_sizer.Add( func_sizer, 1, wx.EXPAND, 5 )
        
        
        top_sizer.Add( module_sizer, 1, wx.EXPAND|wx.LEFT|wx.RIGHT, 5 )
        
        often_sizer = wx.StaticBoxSizer( wx.StaticBox( self.basic_panel, wx.ID_ANY, u"often" ), wx.VERTICAL )
        
        often_btn_sizer = wx.FlexGridSizer( 0, 2, 0, 0 )
        often_btn_sizer.SetFlexibleDirection( wx.BOTH )
        often_btn_sizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        
        self.edit_host = wx.Button( self.basic_panel, wx.ID_ANY, u"edit host", wx.DefaultPosition, wx.DefaultSize, 0 )
        often_btn_sizer.Add( self.edit_host, 0, wx.ALL, 5 )
        
        self.auto_run = wx.Button( self.basic_panel, wx.ID_ANY, u"auto run", wx.DefaultPosition, wx.DefaultSize, 0 )
        often_btn_sizer.Add( self.auto_run, 0, wx.ALL, 5 )
        
        self.advt_setting = wx.Button( self.basic_panel, wx.ID_ANY, u"advt setting", wx.DefaultPosition, wx.DefaultSize, 0 )
        often_btn_sizer.Add( self.advt_setting, 0, wx.ALL, 5 )
        
        
        often_sizer.Add( often_btn_sizer, 1, wx.EXPAND, 5 )
        
        
        top_sizer.Add( often_sizer, 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 5 )
        
        
        basic_sizer.Add( top_sizer, 0, wx.EXPAND, 5 )
        
        bottom_sizer = wx.BoxSizer( wx.VERTICAL )
        
        self.message_box = wx.TextCtrl( self.basic_panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( -1,-1 ), wx.TE_MULTILINE )
        bottom_sizer.Add( self.message_box, 1, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, 5 )
        
        
        basic_sizer.Add( bottom_sizer, 1, wx.EXPAND, 5 )
        
        
        self.basic_panel.SetSizer( basic_sizer )
        self.basic_panel.Layout()
        basic_sizer.Fit( self.basic_panel )
        hSizer.Add( self.basic_panel, 1, wx.EXPAND |wx.ALL, 5 )
        
        self.advt_panel = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        self.advt_panel.Hide()
        
        self.advt_sizer = wx.BoxSizer( wx.HORIZONTAL )
        
        self.advt_notebook = wx.Notebook( self.advt_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
        
        self.advt_sizer.Add( self.advt_notebook, 1, wx.EXPAND |wx.ALL, 5 )
        
        advt_often_sizer = wx.StaticBoxSizer( wx.StaticBox( self.advt_panel, wx.ID_ANY, u"often" ), wx.VERTICAL )
        
        self.basic_setting = wx.Button( self.advt_panel, wx.ID_ANY, u"basic setting", wx.DefaultPosition, wx.DefaultSize, 0 )
        advt_often_sizer.Add( self.basic_setting, 0, wx.ALL, 5 )
        
        self.open_cmd = wx.Button( self.advt_panel, wx.ID_ANY, u"open cmd", wx.DefaultPosition, wx.DefaultSize, 0 )
        advt_often_sizer.Add( self.open_cmd, 0, wx.ALL, 5 )
        
        
        self.advt_sizer.Add( advt_often_sizer, 0, wx.ALL|wx.EXPAND|wx.RIGHT, 5 )
        
        
        self.advt_panel.SetSizer( self.advt_sizer )
        self.advt_panel.Layout()
        self.advt_sizer.Fit( self.advt_panel )
        hSizer.Add( self.advt_panel, 1, wx.EXPAND |wx.ALL, 5 )
        
        
        self.SetSizer( hSizer )
        self.Layout()
        self.status_bar = self.CreateStatusBar( 1, wx.ST_SIZEGRIP, wx.ID_ANY )
        
        self.Centre( wx.BOTH )
        
        # Connect Events
        self.start_all_service.Bind( wx.EVT_BUTTON, self.start_all_service_click )
        self.stop_all_service.Bind( wx.EVT_BUTTON, self.stop_all_service_click )
        self.edit_host.Bind( wx.EVT_BUTTON, self.edit_host_click )
        self.auto_run.Bind( wx.EVT_BUTTON, self.auto_run_click )
        self.advt_setting.Bind( wx.EVT_BUTTON, self.advt_setting_click )
        self.basic_setting.Bind( wx.EVT_BUTTON, self.basic_setting_click )
        self.open_cmd.Bind( wx.EVT_BUTTON, self.open_cmd_click )
    
    def __del__( self ):
        pass
    
    
    # Virtual event handlers, overide them in your derived class
    def start_all_service_click( self, event ):
        event.Skip()
    
    def stop_all_service_click( self, event ):
        event.Skip()
    
    def edit_host_click( self, event ):
        event.Skip()
    
    def auto_run_click( self, event ):
        event.Skip()
    
    def advt_setting_click( self, event ):
        event.Skip()
    
    def basic_setting_click( self, event ):
        event.Skip()
    
    def open_cmd_click( self, event ):
        event.Skip()
    

