import logging
import tkinter

class UiHandler(logging.Handler):
    '''Ui日志处理器

    可以把日志输出到Text控件中
    '''

    def __init__(self, ctrl):
        super().__init__()
        self.ctrl = ctrl

    def emit(self, record):
        if record.getMessage() not in ["", "None"]:
            log_str = self.format(record)
            if isinstance(self.ctrl, tkinter.Text):
                self.ctrl.insert("insert", log_str)
