import time

from core.interface.tools import Logger
from data.constants.status_code import StatusCode as Code


class StatusCodeLogger(Logger):
    def log(self, status_code: Code):
        print(status_code.get_msg())


class DiaryLogger(Logger):
    def log(self, msg):
        now=time.localtime()
        
        pass

