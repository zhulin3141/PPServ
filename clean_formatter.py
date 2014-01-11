import logging
from globals import *

class CleanFormatter(logging.Formatter):

    def format(self, record):
        return super().format(record).replace('\n', ' ') + "\n"
