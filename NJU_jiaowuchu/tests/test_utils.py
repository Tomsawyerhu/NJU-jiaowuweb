from jiaowu.core.function.utils.others import crawl_renew_discuss_and_public_id_reflection, \
    crawl_renew_read_id_reflection
from jiaowu.core.model.login_model import LoginInitializer
from twisted.trial import unittest

from jiaowu.core.model.spider_model import LoginSpider


class ConsoleTest(unittest.TestCase):
    def setUp(self):
        username = "181250002"
        pwd = "7958069Az"
        initializer = LoginInitializer(username, pwd)
        cookie = initializer.start_session()
        self.spider = LoginSpider(cookie)
        self.spider.start_task()

    def test_renew_discuss(self):
        # 测试爬取导学，研讨，通识课程对应id表
        crawl_renew_discuss_and_public_id_reflection(self.spider, 1)

    def test_renew_open(self):
        # 测试爬取公选课程对应id表
        crawl_renew_discuss_and_public_id_reflection(self.spider, -1)

    def test_renew_read(self):
        # 测试爬取经典悦读课程对应id表
        crawl_renew_read_id_reflection(spider=self.spider)


