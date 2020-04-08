"""
程序入口
"""
from core.function.upload.upload_functions import cancel_exam_only_application
from core.model.login_model import LoginInitializer
from core.model.spider_model import LoginSpider

if __name__ == '__main__':
    initializer=LoginInitializer("181250046", "Hhc85851765")
    cookie = initializer.start_session()
    spider = LoginSpider(cookie)
    spider.start_task()
    cancel_exam_only_application(spider,course_id='12345')
    print("任务结束")