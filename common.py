#!/usr/bin/env python
# coding:utf-8

import os
import re
import sys
import codecs
import _winreg
import json
import subprocess
import collections


VERSION = '1.1'
APPNAME = 'PPServ'
BASE_DIR = os.getcwd() + '\\'

def singleton(cls, *args, **kw):
    instances = {}
    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]
    return _singleton

comment_re = re.compile(
    '(^)?[^\S\n]*/(?:\*(.*?)\*/[^\S\n]*|/[^\n]*)($)?',
    re.DOTALL | re.MULTILINE
)

def load_json(file_path):
    '''解析json文件
    首先去除注释再用json模块
    注释示例：
        //...
        或
        /*
        ...
        */
    '''
    with codecs.open(file_path,'r','utf-8') as file:
        content = ''.join(file.readlines())

        match = comment_re.search(content)
        while match:
            content = content[:match.start()] + content[match.end():]
            match = comment_re.search(content)

        return json.loads(content, object_pairs_hook=collections.OrderedDict)

def open_hosts(event):
    '''打开hosts文件'''
    hostfile = os.environ['SYSTEMROOT'] + '\system32\drivers\etc\hosts'
    os.system('notepad %s' % hostfile)

def set_autorun(event):
    '''设置为开机启动'''
    start = sys.argv[0]
    run_key_str = r'Software\Microsoft\Windows\CurrentVersion\Run'
    try:
        run_key = _winreg.OpenKey(HKEY_CURRENT_USER, run_key_str, 0, KEY_ALL_ACCESS)
    except:
        run_key = _winreg.CreateKey(_winreg.HKEY_CURRENT_USER, run_key_str)
    _winreg.SetValueEx(run_key, APPNAME, 0, _winreg.REG_SZ, start)
    _winreg.CloseKey(run_key)

def open_main_page(event):
    '''用默认浏览器打开设置的主页'''
    import webbrowser
    port = '80'
    webbrowser.open("http://localhost:%s" % port)

def execute(cmd, charset='utf-8'):
    '''用命令提示符执行命令

    Args:
        cmd: 执行的命令
        charset: 编码

    Returns:
        执行的结果
    '''
    result = ''
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in p.stdout.readlines():
        result += line.decode(charset)
    return result
