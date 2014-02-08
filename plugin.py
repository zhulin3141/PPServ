#coding:utf-8

class Plugin(object):
    """ 定义一个接口，其他 插件必须实现这个接口，name 属性必须赋值 """
    name = ''
    description = ''
    author = ''
    email = ''
    version = ''
    enable = True

    def __init__(self):
        pass

    def start(self, *args, **kwargs):
        pass

    def stop(self):
        pass
