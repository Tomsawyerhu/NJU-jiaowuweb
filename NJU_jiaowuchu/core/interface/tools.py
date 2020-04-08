import abc
from data.code.status_code import StatusCode as Code


class Utils:
    def get_util_type(self):
        if isinstance(self, Parser):
            return "数据解析器"
        elif isinstance(self, Writer):
            return "数据存储器"
        else:
            return "日志打印器"


class Parser(Utils):
    @abc.abstractmethod
    def parse(self, content):
        pass


class Writer(Utils):
    @abc.abstractmethod
    def write(self, content, url):
        pass


class Logger(Utils):
    @staticmethod
    def log(status_code: Code):
        print(status_code.get_msg())



