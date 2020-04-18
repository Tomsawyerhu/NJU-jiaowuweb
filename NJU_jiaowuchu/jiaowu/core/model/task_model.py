import sys
from queue import Queue

from jiaowu.core.model.spider_model import LoginSpider


class TEMeta(type):
    def __init__(cls, *args, **kwargs):
        """
        # 为任务执行类创建一个任务队列和消息队列
        setattr(cls, '__task_queue', Queue())
        setattr(cls, '__msg_queue', Queue())
        """
        # 实现单例
        cls._instance = None
        super(TEMeta, cls).__init__(*args, **kwargs)

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(TEMeta, cls).__call__( *args, **kwargs)
        return cls._instance

    def __new__(mcs, *args, **kwargs):
        return super(TEMeta, mcs).__new__(mcs, *args, **kwargs)


class TaskExecutor(metaclass=TEMeta):
    """
    任务执行类
    """
    spider: LoginSpider

    def __init__(self, spider):
        self.spider = spider
        self.__task_queue = Queue()
        self.__msg_queue = Queue()

    def add_task(self, task):
        # 向任务队列中添加任务
        self.__task_queue.put(task)
        return self

    def __do_task(self):
        # 执行下一个任务
        if not self.__task_queue.empty():
            task = self.__task_queue.get()
            task.do_task(self.__msg_queue, self.spider)
            self.__task_queue.task_done()
        else:
            print("任务队列为空，无可执行任务")

        return self

    def do_tasks(self):
        # 执行所有任务
        for i in range(self.__task_queue.qsize()):
            self.__do_task()
        return self

    def remove_all_tasks(self):
        # 清除剩余任务
        self.__task_queue.empty()
        return self


class Task:
    TASK_NUM = None  # 任务编号
    TASK_ARGS = None  # 任务参数

    def __init__(self, task_type, task_function, args):
        self.function_pointer = task_function
        self.args = args
        self.task_type = task_type

    def do_task(self, msg_queue: Queue, spider: LoginSpider):
        # 执行自身
        # 非存储类任务
        if self.task_type > 0:
            result = self.function_pointer(spider, self.args)
            # download functions
            if result is not None:
                msg_queue.put(result)
        elif self.task_type < 0:
            # 存储类任务
            data = msg_queue.get()
            self.args["data"] = data
            self.function_pointer(spider, self.args)
        else:
            # 状态转移任务
            self.args["spider"] = spider
            self.function_pointer(spider, self.args)


if __name__ == '__main__':
    taskex = TaskExecutor(LoginSpider("12"))
    taskex2 = TaskExecutor(LoginSpider("13"))
    sys.exit(0)
