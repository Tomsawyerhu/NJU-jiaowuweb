from setuptools import setup, find_packages

setup(name = "NJU_jiaowu_helper",
    version = "1.0",
    description = "教务小助手",
    author = "Tomsawyerhu",
    author_email = "181250046@smail.nju.edu.cn",
    url = "",
    packages = find_packages(),
    #'runner' is in the root.
    scripts = ["runner"],
    entry_points={'console_scripts': [
          'login = DrQueue.RedisRun.redis_run:main',
    ]},
    zip_safe=False

)