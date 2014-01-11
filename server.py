#!python3.2.3
import time
import threading
from comm import *
from conf import *
from lang import *
from service_manager import *
from cache import *
from module.module_factory import *
from center_form import *
import ui_handler
import logging
import logging.config
import clean_formatter
from globals import *

@singleton
class Server(Center_Form):
    '''服务器类

    提供一个操作界面控制所属组件

    Attributes:
        curr_state: 当前运行的状态
        icon: 托盘图标
        x,y: 水平和垂直像素偏移
    '''

    SERVER_STOP = 0
    SERVER_SUCC = 1
    SERVER_FAIL = 2

    curr_state = SERVER_STOP

    def __init__(self, root=None):
        super().__init__()
        self.root = root

        self.protocol("WM_DELETE_WINDOW",self.hide)
        self.hide()
        self.init_ui()
        self.setLog()
        self.start()

    def init_ui(self):
        '''设置UI'''
        self.tk.call('package', 'require', 'Winico')
        self.icon = self.tk.call('winico', 'createfrom',
                os.path.join(os.getcwd(), 'icon.ico'))    # New icon resources
        self.tk.call('winico', 'taskbar', 'add',
            self.icon,
            '-callback', (self.register(self.menu_func), '%m', '%x', '%y'),
            '-pos',self.SERVER_STOP,
            '-text','PPServ')

        self.menu = Menu(self, tearoff=0)
        self.menu.add_command(label=Lang().get('main_page'), command=open_main_page)
        self.menu.add_command(label=Lang().get('menu_about'), command=self.show_about)
        self.menu.add_command(label=Lang().get('menu_quit'), command=self.quit)

        self.top_frame = Frame(self)
        self.top_frame.pack(side=TOP, fill='x')

        self.advt_frame = Frame(self)

        self.curr_frame = 'basic'

        self.init_autorun_panel()
        self.init_often_panel()
        self.init_status_panel()
        self.init_advt_panel()

    def init_autorun_panel(self):
        '''初始化自动运行面板'''
        self.autorun_panel = Labelframe(self.top_frame, text=Lang().get('autorun_label'))
        self.autorun_panel.pack(side=LEFT, anchor=NW, padx=5, pady=5, ipadx=5, ipady=5)

        self.moduleFrame = Frame(self.autorun_panel)
        self.moduleFrame.pack(side=LEFT, padx=5)

        #checkbox
        module = Conf().get('module').keys()

        autorun_checkbox = Cache().data['auto_run']

        self.autorun_state_label = {}
        self.autorun = {}
        for i, module_name in enumerate(module):
            self.autorun[module_name] = value = IntVar()
            if module_name in autorun_checkbox:
                value.set(autorun_checkbox[module_name])
            else:
                value.set(0)
            check = Checkbutton(self.moduleFrame, text = module_name, variable = value,
                onvalue = 1, offvalue = 0, width = 15, command=self.change_module_state)
            check.grid(row=i, column=1)

            state_lbl = Label(self.moduleFrame, text='stop', width=12,anchor="center", background='yellow')
            state_lbl.bind('<Button-1>', self.toggle_state)
            state_lbl.grid(row=i, column=2, padx=10)
            setattr(state_lbl,'module_name',module_name)
            self.autorun_state_label[module_name] = state_lbl

        #button
        self.start_all_btn = Button(self.autorun_panel, text=Lang().get('start_all_service'), width=15,
            command=lambda : self.handler_service_list('start'))
        self.start_all_btn.pack(side=LEFT, ipady=30)

        self.stop_all_btn = Button(self.autorun_panel, text=Lang().get('stop_all_service'), width=15,
            command=lambda : self.handler_service_list('stop'))
        self.stop_all_btn.pack(side=LEFT, ipady=30, padx=5)

    def init_often_panel(self):
        '''初始化常用功能面板'''
        self.often_panel = Labelframe(self.top_frame, text=Lang().get('often_label'))
        self.often_panel.pack(side=LEFT, anchor=NW, padx=5, pady=5)

        edit_hosts = Button(self.often_panel, text=Lang().get('edit_hosts'), width=15, command=open_hosts)
        edit_hosts.grid(row=0, column=0, padx=5, pady=3)

        addto_startup = Button(self.often_panel, text=Lang().get('addto_startup'), width=15, command=set_autorun)
        addto_startup.grid(row=1, column=0, padx=5, pady=3)

        advt_setting = Button(self.often_panel, text=Lang().get('advt_setting'), width=15, 
            command=self.change_frame)
        advt_setting.grid(row=2,column=0, padx=5, pady=3)

    def init_status_panel(self):
        '''设置状态面板'''
        self.bottom_frame = Frame(self)
        self.bottom_frame.pack(side=TOP, fill='x')
        scb_msg = Scrollbar(self.bottom_frame)
        scb_msg.pack(side=RIGHT, fill=Y)

        self.msg_box = Text(self.bottom_frame, yscrollcommand = scb_msg.set)
        self.msg_box.pack(fill=BOTH)

        scb_msg.config(command=self.msg_box.yview)

    def init_advt_panel(self):
        module_panel = Frame(self.advt_frame)
        module_panel.pack(side=LEFT, anchor=NW, padx=5, pady=5, ipadx=5, ipady=5)

        advt_func_panel = Labelframe(self.advt_frame, text=Lang().get('often_label'))
        advt_func_panel.pack(side=RIGHT, anchor=NW, padx=5, pady=5, ipadx=15, ipady=5)

        Button(advt_func_panel, text=Lang().get('basic_setting'), command=self.change_frame).pack()

        tabs = Notebook(module_panel)
        for module in ServiceManager().get_module_list():
            module.set_advt_frame(tabs, advt_func_panel)
        tabs.pack()

    def setLog(self):
        '''设置UI界面的消息框和加载配置中的log设置'''
        msg_handler = ui_handler.UiHandler(self.msg_box)
        msg_handler.setFormatter(clean_formatter.CleanFormatter(FORMAT, DATEFMT))
        msg_handler.setLevel(logging.DEBUG)
        logger.addHandler(msg_handler)

        logging.config.dictConfig(Conf().get('logging'))

    def change_module_state(self):
        '''保存选择的运行模块'''
        autorun = {}
        for module_name, val in self.autorun.items():
            autorun[module_name] = val.get()
        Cache().set('auto_run',autorun)

    def toggle_state(self,event):
        module_name = getattr(event.widget,'module_name')
        module = ModuleFactory.factory(module_name)
        state = module.get_state().upper()

        if state == RUNNING:
            ServiceManager().stop_service([module_name])
        elif state == STOPPED:
            ServiceManager().start_service([module_name])
        else:
            pass
        self.msg_box.see(END)

    def change_frame(self):
        if self.curr_frame == 'basic':
            self.top_frame.forget()
            self.bottom_frame.forget()
            self.advt_frame.pack(side=TOP, fill='x')
            self.curr_frame = 'advt'
        else:
            self.top_frame.pack(side=TOP, fill='x')
            self.bottom_frame.pack(side=TOP, fill='x')
            self.advt_frame.forget()
            self.curr_frame = 'basic'

    def check_service(self):
        '''切换状态标签上的状态'''
        update_state = threading.Thread(target=self.update_service_state)
        update_state.setDaemon(True)
        update_state.start()

    def update_service_state(self):
        '''更新服务面板的状态'''
        state_opt = Conf().get('state_style')
        while True:
            for module_name,state_lbl in self.autorun_state_label.items():
                state = ModuleFactory.factory(module_name).get_state()
                state_lbl['text'] = state.lower()
                if state in state_opt:
                    state_lbl.config(state_opt[state])
            time.sleep(3)

    def update_service(self,module_name,module_val,act='start'):
        '''改变服务的状态'''
        if module_val.get() is 1:
            if act == 'start':
                ServiceManager().start_service([module_name])
            else:
                ServiceManager().stop_service([module_name])
            self.msg_box.see(END)

    def handler_service_list(self,act='start'):
        '''启动或停止所选服务'''
        for module_name,module_val in self.autorun.items():
            update_service = threading.Thread(target=self.update_service,args=(module_name,module_val,act))
            update_service.setDaemon(True)
            update_service.start()

    def hide(self):
        '''隐藏UI'''
        self.withdraw()

    def show(self):
        '''显示UI'''
        self.update()
        self.deiconify()

    def show_about(self):
        '''显示关于窗口'''
        about = Center_Form(Toplevel)
        about.title(Lang().get('about_title'))
        about.resizable( False, False )

        title = Label(about, text='PPServ')
        title.config(font=('times', 24, 'italic'))
        title.pack(pady=5)

        about_text = 'zhulin3141@gmail.com\n %s' % VERSION
        label = Label(about, text=about_text)
        label.pack(pady=3)

        about.center_window(400,200)

    def change_state(self,state):
        '''切换状态'''
        self.curr_state = state
        self.tk.call('winico', 'taskbar', 'modify', self.icon,'-pos', self.curr_state, '-text', 'PPServ')

    def start(self):
        ServiceManager().install_service()
        self.msg_box.see(END)

        self.check_service()

        if True :
            self.change_state(self.SERVER_SUCC)
        elif False :
            self.change_state(self.SERVER_FAIL)

    def quit(self):
        '''退出'''
        self.tk.call('winico', 'taskbar', 'delete', self.icon)
        super().quit()

    def menu_func(self,event, x, y):
        '''托盘控制'''
        if event == 'WM_RBUTTONDOWN':    # Right click tray icon, pop up menu
            self.menu.tk_popup(x, y)
        elif event == 'WM_LBUTTONDOWN':
            self.show()

if __name__ == '__main__':
    server = Server()
    server.title(Conf().get('app_name'))
    server.resizable(False, False)
    server.center_window(850,300)
    server.mainloop()
