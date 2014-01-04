#!/usr/bin/env python
# coding:utf-8

import win32service

class ServiceManager(object):
    """管理window服务"""

    def __init__(self, name):
        """
        name: 服务的名称
        """
        self.name = name
        self.scm = win32service.OpenSCManager(None, None, win32service.SC_MANAGER_ALL_ACCESS)
        self.handle = win32service.OpenService(self.scm, self.name, win32service.SC_MANAGER_ALL_ACCESS)

    def IsStop(self):
        """检查服务是否停止"""
        flag = False
        try:
            if self.handle:
                ret = win32service.QueryServiceStatus(self.handle)
                flag = ret[1] != win32service.SERVICE_RUNNING
        except Exception, e:
            print e[2].decode('gb2312').encode('utf-8')
        return flag

    def Start(self):
        """开启服务"""
        try:
            if self.handle:
                win32service.StartService(self.handle, None)
        except Exception, e:
            print e[2].decode('gbk').encode('utf-8')
        return win32service.QueryServiceStatus(self.handle)

    def Stop(self):
        """停止服务"""
        try:
            status = win32service.ControlService(self.handle, win32service.SERVICE_CONTROL_STOP)
        except Exception, e:
            print e[2].decode('gbk').encode('utf-8')
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
            print e

    def Close(self):
        """释放资源"""
        try:
            if self.scm:
                win32service.CloseServiceHandle(self.handle)
                win32service.CloseServiceHandle(self.scm)
        except Exception, e:
            print e
