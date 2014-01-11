import os
import logging

APPNAME = 'PPServ'
VERSION = 'Version 1.0.0'
BASE_DIR = os.getcwd() + '\\'

#运行状态
RUNNING = 'RUNNING'
STOPPED = 'STOPPED'
UNKNOWN = 'UNKNOWN'


FORMAT = "%(asctime)s %(levelname)s %(message)s"
DATEFMT = "%Y-%m-%d %H:%M:%S"

logger = logging.getLogger(__name__)
