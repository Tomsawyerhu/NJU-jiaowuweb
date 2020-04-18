from jiaowu.core.function.utils.others import get_values
from jiaowu.core.model.login_model import LoginInitializer
from jiaowu.core.model.spider_model import LoginSpider


def switch_account(spider: LoginSpider, args):
    spider: LoginSpider
    values = get_values(args, ["username", "password", "spider"])
    username, pwd, spider = tuple(values)

    initializer = LoginInitializer(username, pwd)
    cookie = initializer.start_session()
    if cookie is None:
        print("保持原登录状态")
    else:
        spider.set_cookie(cookie)
        print("切换用户至(%s,%s)"%(username,pwd))
        spider.start_task()
