"""
程序入口
"""
import core.function.upload.upload_functions as functions
from core.model.login_model import LoginInitializer
from core.model.spider_model import LoginSpider

if __name__ == '__main__':
    initializer=LoginInitializer("181250046", "Hhc85851765")
    cookie = initializer.start_session()
    spider = LoginSpider(cookie)
    spider.start_task()
    functions.update_password(spider=spider,old_pwd='Hhc85851765',new_pwd='Hhc85851765')
    print("任务结束")