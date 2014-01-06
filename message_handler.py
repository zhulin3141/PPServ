#!/usr/bin/env python
# coding:utf-8

import time
import logging

class MessageHandler(logging.Handler):
    def __init__(self, obj):
        logging.Handler.__init__(self);
        self.Object = obj

    def emit(self, record):
        tstr = time.strftime('%Y-%m-%d %H:%M:%S:%U')
        self.Object.AppendText("[%s][%s] %s\n" % (tstr, record.levelname, record.getMessage()))
