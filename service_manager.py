#!/usr/bin/env python
# coding:utf-8
#Requires pywin32 http://sourceforge.net/projects/pywin32/files/pywin32/Build%20218/
import win32service
import win32con
import logging
from conf import *

class ServiceManager(object):
    """管理window服务"""

    def __init__(self, name):
        """
        name: 服务的名称
        """
        self.name = name
        self.encode = Conf().get('encoding')
        self.scm = win32service.OpenSCManager(None, None, win32service.SC_MANAGER_ALL_ACCESS)
        try:
            self.handle = win32service.OpenService(self.scm, self.name, win32service.SC_MANAGER_ALL_ACCESS)
        except Exception, e:
            self.Log(e)

    def IsStop(self):
        """检查服务是否停止"""
        flag = False
        try:
            if self.handle:
                ret = win32service.QueryServiceStatus(self.handle)
                flag = ret[1] != win32service.SERVICE_RUNNING
        except Exception, e:
            self.Log(e)
        return flag

    def Start(self):
        """开启服务"""
        try:
            if self.handle:
                win32service.StartService(self.handle, None)
        except Exception, e:
            self.Log(e)
        return win32service.QueryServiceStatus(self.handle)

    def Stop(self):
        """停止服务"""
        try:
            status = win32service.ControlService(self.handle, win32service.SERVICE_CONTROL_STOP)
        except Exception, e:
            self.Log(e)
        return status

    def Restart(self):
        """重启服务"""
        if not self.IsStop():
            self.Stop()
        self.Start()
        return win32service.QueryServiceStatus(self.handle)

    def Status(self):
        """获取运行的状态"""
        try:
            statusInfo = win32service.QueryServiceStatus(self.handle)
            status = statusInfo[1]
            if status == win32service.SERVICE_STOPPED:
                return "STOPPED"
            elif status == win32service.SERVICE_START_PENDING:
                return "STARTING"
            elif status == win32service.SERVICE_STOP_PENDING:
                return "STOPPING"
            elif status == win32service.SERVICE_RUNNING:
                return "RUNNING"
        except Exception, e:
            self.Log(e)

    def Close(self):
        """释放资源"""
        try:
            if self.scm:
                win32service.CloseServiceHandle(self.handle)
                win32service.CloseServiceHandle(self.scm)
        except Exception, e:
            self.Log(e)

    def IsExists(self):
        """windows服务是否已安装"""
        statuses = win32service.EnumServicesStatus(self.scm, win32service.SERVICE_WIN32, win32service.SERVICE_STATE_ALL)
        for (short_name, desc, status) in statuses:
            if short_name == self.name:
                return True
        return False

    def Log(self, exception):
        logging.exception(exception[2].decode(self.encode).encode('utf-8'))
