#!/usr/bin/env python
# coding:utf-8

from common import *
from lang import *
import re
import logging
from service_manager import *
import wx

class BaseModule(object):
    '''模块类

    根据配置文件中的module配置的模块

    Attrs:
        module_name: 模块名,配置文件中的key
        service_name: 安装为服务的名称
        group: 模块分组，分组名为模块的名称，如PHP5.3，PHP4的模块分组都是php
        path: 软件所在的目录
        install: 作为服务安装的命令
        uninstall: 卸载服务的命令
        serviceManager: 服务管理
        setting_panel: 设置panel
    '''

    def __init__(self, name):
        '''根据名称加载配置中的数据初始化类'''
        try:
            conf_data = BaseModule.list_module_data()[name]
            self.module_name = name
            self.setting_panel = None
            self.setting_sizer = wx.BoxSizer(wx.HORIZONTAL)
        except:
            print(Lang().get('module_load_error'))
        
        if conf_data is not None:
            for attr,val in conf_data.items():
                setattr(self, attr, val)

        if hasattr(self, 'service_name'):
            self.serviceManager = ServiceManager(self.service_name)

    @staticmethod
    def list_module_data():
        return load_json('conf/conf.json')['module']

    @staticmethod
    def list_service_module():
        service_list = []
        for mod_name, mod in load_json('conf/conf.json')['module'].items():
            if 'service_name' in mod:
                service_list.append(mod_name)
        return service_list

    def install_service(self):
        '''安装模块的服务

        如果可以作为服务安装，则执行安装命令
        '''
        if hasattr(self, 'install'):
            if self.install.find('%s') is -1:
                return execute(self.install).strip()
            else:
                return execute(self.install % BASE_DIR).strip()

    def uninstall_service(self):
        '''卸载模块的服务

        如果服务已安装，并且有卸载命令则执行卸载命令
        '''
        if self.is_install() and hasattr(self, 'uninstall'):
            #卸载服务前先停止服务
            self.stop_service()
            if self.uninstall.find('%s') is -1:
                return execute(self.uninstall).strip()
            else:
                return execute(self.uninstall % BASE_DIR).strip()

    def start_service(self):
        '''启动对应的服务'''
        if hasattr(self, 'service_name'):
            if self.get_state() == RUNNING:
                msg = Lang().get('is_already_running')
            else:
                msg = self.serviceManager.Start()
            logging.info(msg)

    def stop_service(self):
        '''停止对应的服务'''
        if hasattr(self, 'service_name'):
            if self.get_state() == STOPPED:
                msg = Lang().get('is_already_stopped') % self.service_name
            else:
                msg = self.serviceManager.Stop()
            logging.info(msg)

    def is_install(self):
        '''检查服务是否已安装'''
        if hasattr(self, 'service_name'):
            return self.serviceManager.IsExists()
        else:
            return True

    def get_state(self):
        '''
        获取服务运行的状态
        Returns: STOPPED,RUNNING,STARTING,STOPPING,UNKNOWN
        '''
        if hasattr(self, 'service_name'):
            return self.serviceManager.Status()
        else:
            return UNKNOWN

    def set_advt_frame(self, parent):
        self.setting_panel = wx.Panel(parent)

    def replace(self, file, pattern, subst, count=0, flags=re.MULTILINE):
        '''替换文件中的字符串'''
        file_handle = open(file, 'r')
        file_string = file_handle.read()
        file_handle.close()

        file_string = (re.sub(pattern, subst, file_string, count, flags))

        file_handle = open(file, 'w')
        file_handle.write(file_string)
        file_handle.close()

