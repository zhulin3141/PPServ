#coding:utf-8
import sys
sys.path.append('../')

from plugin import Plugin

__all__ = ["FirstPlugin"]

class FirstPlugin(Plugin):

    name = "firstPlugin"
    version = '0.0.1'

    def __init__(self):
        Plugin.__init__(self)

    def scan(self, config={}):
        return "first plugin"

    def start(self, *args, **kwargs):
        print self.name + ' is running... \n params is '
        print args, kwargs
