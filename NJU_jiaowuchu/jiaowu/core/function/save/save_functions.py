from jiaowu.core.function.utils.formatter import ClassInfoFormatter
from jiaowu.core.function.utils.others import get_values
from jiaowu.core.function.utils.writer import TBExcelWriter
from jiaowu.core.model.spider_model import LoginSpider


def save_as_excel(spider: LoginSpider, args):
    file_path, data, data_type = tuple(get_values(args, ["file_path", "data", "data_type"]))
    if data_type == '1':
        # 课程表
        writer = TBExcelWriter()
        writer.write(data, file_path)
    elif data_type == '2':
        # todo
        pass
    else:
        pass


def save_as_pdf(spider: LoginSpider, args):
    pass


def save_as_json(spider: LoginSpider, args):
    pass
