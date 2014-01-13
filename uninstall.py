#!/usr/bin/env python
# coding:utf-8

from module.module_factory import *

for mod in ModuleFactory.get_module_list():
    if mod.is_install():
        print mod.uninstall_service()
