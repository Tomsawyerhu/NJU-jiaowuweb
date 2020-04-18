from jiaowu.console.instruction import Instruction
from jiaowu.core.model.login_model import LoginInitializer
from jiaowu.core.model.spider_model import LoginSpider
from jiaowu.core.model.task_model import TaskExecutor

instruction_buffer = []


def main():
    print("welcome to NJUjaowu helper system！\nplease login")
    username = input("Username:")
    pwd = input("Password:")
    initializer = LoginInitializer(username, pwd)
    cookie = initializer.start_session()

    # 用户名或密码错误重新输入
    while cookie is None:
        print("请重新输入用户名密码")
        username = input("Username:")
        pwd = input("Password:")
        initializer.set_username(username)
        initializer.set_passwd(pwd)
        cookie = initializer.start_session()

    spider = LoginSpider(cookie)
    spider.start_task()
    task_executor = TaskExecutor(spider=spider)
    wait(task_executor=task_executor)


def wait(task_executor: TaskExecutor):
    end = False
    print("NJUjwc>>")
    raw_instruction_str = input().strip()
    instruction_str = ""
    if raw_instruction_str.endswith(';'):
        end = True
        instruction_str = raw_instruction_str[0:len(raw_instruction_str) - 1]
    else:
        instruction_str = raw_instruction_str

    instruction = Instruction(instruction_str)
    if not instruction.is_valid():
        # rollback
        print("wrong instruction format,please enter [INSTRUCTION_NAME]? for help")
        wait(task_executor)
    else:
        task = instruction.to_task()
        task_executor.add_task(task)
        if end:
            task_executor.do_tasks()
            print("所有任务已完成")
        wait(task_executor)


if __name__ == '__main__':
    main()
