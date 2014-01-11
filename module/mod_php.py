from comm import *
from module.module import *
from tkinter import *
from tkinter.ttk import *

class Mod_Php(Module):
    '''PHP模块类'''
    def __init__(self, name):
        Module.__init__(self, name)
        self.conf_file = BASE_DIR + self.path + "\php.ini"

    def set_advt_frame(self,parent,fun):
        php_tab = Frame(parent)
        php_tab.place(x=10,y=10)

        cvs = Canvas(php_tab)
        php_extension = Frame(cvs)
        sbar = Scrollbar(php_tab, orient="vertical", command=cvs.yview)
        cvs.configure(yscrollcommand=sbar.set, highlightthickness=0)
        cvs.bind_all("<MouseWheel>", lambda event, wrap=cvs: self.on_mouse_wheel(event, wrap))

        sbar.pack(side="right", fill="y")
        cvs.pack(side="left")
        cvs.create_window((0,0), window=php_extension, anchor='nw')
        php_extension.bind("<Configure>", lambda event, frame=cvs: self.scroll(event, frame))

        content = open(self.conf_file,'r').read()
        mod = re.findall('(^;*)extension=(php_.*).dll', content, re.M)
        self.module_list = {}
        for (is_loaded, mod_name) in mod:
            self.module_list[mod_name] = value = IntVar()
            if is_loaded.strip() == '':
                value.set(1)
            else:
                value.set(0)
            ckb = Checkbutton(php_extension, text=mod_name, variable = value, onvalue = 1, offvalue = 0, width = 25)
            ckb.pack()
            ckb.bind('<Button-1>', self.change_module_state)

        parent.add(php_tab, text=self.module_name)

    def change_module_state(self,event):
        chb = event.widget
        module_name = chb['text']
        value = self.module_list[module_name].get()

        if value is 0:
            self.replace(self.conf_file, r';+extension=' + module_name, 'extension=' + module_name)
        else:
            self.replace(self.conf_file, r'extension=' + module_name, ';extension=' + module_name)
