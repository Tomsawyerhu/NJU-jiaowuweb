import json
import os

import requests

from jiaowu.data.config import task_config


class LoginSpider:
    def __init__(self, cookies):
        self.cookies = cookies
        self.task = None

    def set_cookie(self, cookie):
        self.cookies = cookie

    def start_task(self):
        header_template = task_config.headers
        self.task = requests.session()
        self.task.headers = {
            "Accept": header_template["Accept"],
            "Accept-Language": header_template["Accept-Language"],
            "Upgrade-Insecure-Requests": header_template["Upgrade-Insecure-Requests"],
            "User-Agent": header_template["User-Agent"],
            "Accept-Encoding": header_template["Accept-Encoding"],
            "Host": header_template["Host"],
            # "Cookie": self.cookies,
            "Connection": header_template["Connection"]
        }
        self.task.cookies = self.cookies

    def terminate_task(self):
        self.task.close()

    def update_header(self, key, value):
        """
        向headers中添加或修改属性，本场景下是Refer字段
        :param key:header属性名
        :param value:header属性值
        :return:null
        """
        self.task.headers[key] = value
