from comm import *
from module.module import *
from tkinter import *
from tkinter.ttk import *
import re

class Mod_Apache(Module):
    '''Apache模块类'''
    def __init__(self, name):
        Module.__init__(self, name)
        self.conf_file = BASE_DIR + self.path + "\conf\httpd.conf"

    def set_advt_frame(self,parent,fun):
        apache_tab = Frame(parent)
        apache_tab.place(x=10,y=10)

        cvs = Canvas(apache_tab)
        apache_module = Frame(cvs)
        self.sbar = Scrollbar(apache_tab, orient="vertical", command=cvs.yview)
        cvs.configure(yscrollcommand=self.sbar.set, highlightthickness=0)
        cvs.bind_all("<MouseWheel>", lambda event, wrap=cvs: self.on_mouse_wheel(event, wrap))

        self.sbar.pack(side="right", fill="y")
        cvs.pack(side="left")
        cvs.create_window((0,0), window=apache_module, anchor='nw')
        apache_module.bind("<Configure>", lambda event, frame=cvs: self.scroll(event, frame))

        content = open(self.conf_file,'r').read()
        mod = re.findall('(^#*)LoadModule (.+_module)', content, re.M)
        self.module_list = {}
        for (is_loaded, mod_name) in mod:
            self.module_list[mod_name] = value = IntVar()
            if is_loaded.strip() == '':
                value.set(1)
            else:
                value.set(0)
            ckb = Checkbutton(apache_module, text=mod_name, variable = value, onvalue = 1, offvalue = 0, width = 25)
            ckb.pack()
            ckb.bind('<Button-1>', self.change_module_state)

        parent.add(apache_tab, text=self.module_name)

    def change_module_state(self,event):
        '''设置模块是否加载

        如果选中则加载
        如果未选中则取消加载'''
        chb = event.widget
        module_name = chb['text']
        value = self.module_list[module_name].get()

        if value is 0:
            self.replace(self.conf_file, r'#+LoadModule ' + module_name, 'LoadModule ' + module_name)
        else:
            self.replace(self.conf_file, r'LoadModule ' + module_name, '#LoadModule ' + module_name)
