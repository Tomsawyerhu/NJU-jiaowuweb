from abc import abstractmethod

from core.model.login_model import LoginSpider


class UploadTask:
    """
    信息上传任务基类
    """

    @abstractmethod
    def do_task(self, task_name):
        pass


class DownloadTask:
    """
    信息下载任务基类
    """

    def __init__(self):
        self.parser = None
        self.writer = None
        self.raw_data = None

    def set_parser(self, parser):
        self.parser = parser

    def set_writer(self, writer):
        self.writer = writer

    @abstractmethod
    def do_task(self, task_name):
        pass

    def save(self, url=None):
        if url is None or self.writer is None:
            pass
        else:
            data = None
            if self.parser is not None:
                data = self.parser.parse(self.raw_data)
            else:
                data = self.raw_data
            self.writer.write(data, url)
