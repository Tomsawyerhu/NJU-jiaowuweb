import json
import re

from scrapy import Selector
import requests
from requests.cookies import cookiejar_from_dict
from code.status_code import StatusCode as code

'''
功能表：
1.下载通知新闻
2.下载课程信息
3.查看成绩单
4.申请/取消免修不免靠
5.
'''

class Course:
    def __init__(self, id=None, name=None, mark=None, type=None, credit=None, teacher=None, time_and_loc=None,comments=None):
        self.id = id
        self.name = name
        self.mark = mark
        self.type = type
        self.credit = credit
        self.teacher = teacher
        self.time_and_loc = time_and_loc
        self.comments=comments


class LoginSpider:
    def __init__(self, cookies):
        self.cookies = cookies
        self.task = None

    def start_task(self):
        config_file = open("./config/task_config.json", 'r')
        config_json = json.load(config_file)
        self.task = requests.session()
        self.task.headers = {
            "Accept": config_json["Accept"],
            "Accept-Language": config_json["Accept-Language"],
            "Upgrade-Insecure-Requests": config_json["Upgrade-Insecure-Requests"],
            "User-Agent": config_json["User-Agent"],
            "Accept-Encoding": config_json["Accept-Encoding"],
            "Host": config_json["Host"],
            # "Cookie": self.cookies,
            "Connection": config_json["Connection"]
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

    def crawl_news(self, start=0, end=100):
        # 爬取首页通知
        return 0

    def check_grades(self, year, term):
        # 查看成绩
        course_list = []
        self.update_header("Referer", "http://elite.nju.edu.cn/jiaowu/student/studentinfo/index.do")
        response = self.task.get(
            url="http://elite.nju.edu.cn/jiaowu/student/studentinfo/achievementinfo.do?method=searchTermList" + "&termCode=" + str(
                year) + str(term))
        grades_table = Selector(text=response.text).xpath("//tr[@class='TABLE_TR_01']") + Selector(
            text=response.text).xpath("//tr[@class='TABLE_TR_02']")
        for selector in grades_table:
            course = Course()
            tds = selector.xpath("./td")
            # print(len(tds))
            course.id = tds[1].xpath("./a/u/text()")[0].extract()
            # print(course.id)
            course.name = tds[2].xpath("./text()")[0].extract()
            # print(course.name)
            course.type = tds[4].xpath("./text()")[0].extract().strip()
            # print(course.type)
            credit = tds[5].xpath("./text()").extract()
            if len(credit) > 0:
                course.credit = credit[0]
            print(course.credit)
            course.mark = tds[6].xpath("./ul/text()")[0].extract().strip()
            # print(course.mark)
            course_list.append(course)

        # print(grades_table)
        return course_list

    def get_timetable(self):
        self.update_header("Referer", "http://elite.nju.edu.cn/jiaowu/student/teachinginfo/index.do")
        response = self.task.get(
            url="http://elite.nju.edu.cn/jiaowu/student/teachinginfo/courseList.do?method=currentTermCourse")
        course_table = Selector(text=response.text).xpath("//tr[@class='TABLE_TR_01']") + Selector(
            text=response.text).xpath("//tr[@class='TABLE_TR_02']")
        course_list=[]
        for selector in course_table:
            course = Course()
            tds = selector.xpath("./td")
            # print(len(tds))
            course.id = tds[0].xpath("./a/u/text()")[0].extract().strip()
            # print(course.id)
            course.name = tds[1].xpath("./text()")[0].extract().strip()
            # print(course.name)
            course.teacher = tds[3].xpath("./text()")[0].extract().strip()
            # print(course.teacher)
            time_and_loc = tds[4].xpath("./text()")
            str=""
            for s in time_and_loc:
                str+=s.extract().strip()+"\n"
            course.time_and_loc=str
            # print(course.time_and_loc)
            course.type = tds[6].xpath("./text()")[0].extract().strip()
            # print(course.type)
            comments=tds[8].xpath("./b/text()")
            if len(comments)>0:
                course.comments=comments[0].extract().strip()
            # print(course.comments)
            course_list.append(course)
        return course_list

    def apply_for_exam_only(self,course_name=None,course_id=None):
        #申请免修不免靠
        self.update_header("Referer",'http://elite.nju.edu.cn/jiaowu/student/elective/index.do')
        response=self.task.get(url="http://elite.nju.edu.cn/jiaowu/student/teachinginfo/courseList.do?method=exemptionBMKList")
        selector=Selector(text=response.text)
        trs=selector.xpath("//tr[@align='left']")
        class_id=""
        for tr in trs:
            if tr.xpath("./td/text()")[0].extract()==course_id or tr.xpath("./td/text()")[1].extract()==course_name:
                class_id=re.search(re.compile("\((\d+)\)"),tr.xpath("./td")[3].xpath("./a/@href")[0].extract()).group(1)
        if len(class_id)>0:
            # 检测已申请的课程是否在规定数量之内
            if len(selector.xpath("//div[@id='courseList']")[0].css("table tr[align='left']"))>=2:
                print(code.APPLICATION_BEYOND_MAX_LIMITS.get_msg())
                return
            self.task.get(url="http://elite.nju.edu.cn/jiaowu/student/teachinginfo/courseList.do?method=exemptionBMKApply&classId=%s"%class_id)
        else:
            print(code.COURSE_NOT_FOUND.get_msg())

    def cancel_exam_only_application(self,course_name=None,course_id=None):
        # 取消免修不免靠申请
        self.update_header("Referer", 'http://elite.nju.edu.cn/jiaowu/student/elective/index.do')
        response = self.task.get(
            url="http://elite.nju.edu.cn/jiaowu/student/teachinginfo/courseList.do?method=exemptionBMKList")
        selector = Selector(text=response.text)
        trs = selector.xpath("//tr[@align='left']")
        class_id = ""
        for tr in trs:
            if tr.xpath("./td/text()")[0].extract() == course_id or tr.xpath("./td/text()")[1].extract() == course_name:
                class_id = re.search(re.compile("\((\d+)\)"),
                                     tr.xpath("./td")[3].xpath("./a/@href")[0].extract()).group(1)
        if len(class_id) > 0:
            # 检测是否在待审核列表
            application_list=selector.xpath("//div[@id='courseList']/table")[0].css("tr[align='left']")
            flag=False
            for application in application_list:
                tds_text=application.xpath("./td/text()").extract()
                if tds_text[0]==course_id or tds_text[1]==course_name:
                    flag=True
            if not flag:
                print(code.COURSE_NOT_EXIST_IN_LIST.get_msg())
                return
            self.task.get(
                url="http://elite.nju.edu.cn/jiaowu/student/teachinginfo/courseList.do?method=exemptionBMKDelete&classId=%s" % class_id)
        else:
            print(code.COURSE_NOT_FOUND.get_msg())




