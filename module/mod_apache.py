#!/usr/bin/env python
# coding:utf-8

from common import *
from base_module import BaseModule
import re

class Mod_Apache(BaseModule):
    '''Apache模块类'''
    def __init__(self, name):
        BaseModule.__init__(self, name)
        self.conf_file = BASE_DIR + self.path + "\conf\httpd.conf"
