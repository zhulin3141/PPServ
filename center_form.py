from tkinter import *
from tkinter.ttk import *

class Center_Form(Tk):
    def __init__(self, cls=None):
        super().__init__()
        if cls is not None:
            Center_Form.__bases__ = (cls,) + Center_Form.__bases__

    def center_window(self, w=300, h=200):
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()

        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        self.geometry('%dx%d+%d+%d' % (w, h, x, y))
