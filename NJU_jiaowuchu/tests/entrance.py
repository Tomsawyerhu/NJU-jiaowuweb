"""
程序入口
"""
from jiaowu.core.function.download.download_functions import check_course_info
from jiaowu.core.model.login_model import LoginInitializer
from jiaowu.core.model.spider_model import LoginSpider

if __name__ == '__main__':
    initializer=LoginInitializer("181250046", "Hhc85851765")
    cookie = initializer.start_session()
    spider = LoginSpider(cookie)
    spider.start_task()
    check_course_info(spider,2018,1,2018,"软件工程")
    print("任务结束")