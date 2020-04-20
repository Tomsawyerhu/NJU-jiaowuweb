import json
import os
from scrapy import Selector

from jiaowu.core.function.utils.others import crawl_speciality_select, get_values
from jiaowu.core.model.data_model import Course
from jiaowu.core.model.spider_model import LoginSpider


# 下载信息功能
def check_grades(spider: LoginSpider, args):
    # 查看成绩
    values = get_values(args, ["year", "term"])
    year, term = tuple(values)

    course_list = []
    spider.update_header("Referer", "http://elite.nju.edu.cn/jiaowu/student/studentinfo/index.do")
    response = spider.task.get(
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
        # print(course.credit)
        course.mark = tds[6].xpath("./ul/text()")[0].extract().strip()
        # print(course.mark)
        course_list.append(course)

    # print(grades_table)
    return course_list


def get_timetable(spider: LoginSpider, args):
    # 下载课程表
    spider.update_header("Referer", "http://elite.nju.edu.cn/jiaowu/student/teachinginfo/index.do")
    response = spider.task.get(
        url="http://elite.nju.edu.cn/jiaowu/student/teachinginfo/courseList.do?method=currentTermCourse")
    course_table = Selector(text=response.text).xpath("//tr[@class='TABLE_TR_01']") + Selector(
        text=response.text).xpath("//tr[@class='TABLE_TR_02']")
    course_list = []
    for selector in course_table:
        course = Course()
        tds = selector.xpath("./td")
        # print(len(tds))
        course.id = tds[0].xpath("./a/u/text()")[0].extract().strip()
        # print(course.id)
        course.name = tds[1].xpath("./text()")[0].extract().strip()
        # print(course.name)
        course.teacher = tds[3].xpath("./text()")[0].extract()
        # print(course.teacher)
        time_and_loc = tds[4].xpath("./text()")
        str = ""
        for s in time_and_loc:
            str += s.extract().strip() + "\n"
        course.time_and_loc = str
        # print(course.time_and_loc)
        course.type = tds[6].xpath("./text()")[0].extract().strip()
        # print(course.type)
        comments = tds[8].xpath("./b/text()")
        if comments is not None and len(comments) > 0:
            course.comments = comments[0].extract().strip()
        # print(course.comments)
        course_list.append(course)
    return course_list


def crawl_news(spider: LoginSpider, args):
    # 爬取首页通知
    return 0


def check_course_info(spider: LoginSpider, args):
    # 查询院系课程
    values = get_values(args, ["year", "term", "grade", "major"])
    year, term, grade, major = tuple(values)

    spider.update_header("Referer",
                         "http://elite.nju.edu.cn/jiaowu/student/teachinginfo/allCourseList.do?method=getTermAcademy")

    # todo 此段硬编码需修改
    curPath = os.path.abspath(os.path.dirname(__file__))
    paths_part = curPath.split('\\')
    for i in range(3):
        paths_part.pop()
    rootPath = '\\'.join(paths_part)
    reflection_json_path = rootPath + "\\data\\output\\reflection.json"
    if not os.path.exists(reflection_json_path):
        crawl_speciality_select(spider)
    fp = open(reflection_json_path, 'r', encoding="utf-8")

    major_index = json.load(fp)[major]
    url = "http://elite.nju.edu.cn/jiaowu/student/teachinginfo/allCourseList.do?method=getCourseList" + "&curTerm=" + str(
        year) + str(term) + "&curSpeciality=" + major_index + "&curGrade=" + str(grade)
    response = spider.task.get(url=url)
    selector = Selector(text=response.text)
    course_selectors = selector.xpath("//tr[@class='TABLE_TR_01']") + selector.xpath("//tr[@class='TABLE_TR_02']")
    course_list = []

    # 注意检查未开课的院系
    if len(course_selectors) <= 1:
        return course_list

    for selector in course_selectors:
        tds = selector.css("td")
        course = Course()
        course.id = tds[0].css("a>u::text")[0].get().strip()
        course.name = tds[1].xpath("./text()").get().strip()
        course.type = tds[2].xpath("./text()").get().strip()
        course.host = tds[3].xpath("./text()").get()
        course.credit = tds[4].xpath("./text()").get()
        course.hours = tds[5].xpath("./text()").get().strip()
        course.district = tds[6].xpath("./text()").get()
        course.teacher = tds[7].xpath("./text()").get()
        course.time_and_loc = tds[8].xpath("./text()").get()
        # print(course)
        course_list.append(course)
    return course_list


def check_all_course_info(spider: LoginSpider, args):
    # 返回全校课程
    course_list = []

    # todo 此段硬编码需修改
    curPath = os.path.abspath(os.path.dirname(__file__))
    paths_part = curPath.split('\\')
    for i in range(3):
        paths_part.pop()
    rootPath = '\\'.join(paths_part)
    reflection_json_path = rootPath + "\\data\\output\\reflection.json"
    if not os.path.exists(reflection_json_path):
        crawl_speciality_select(spider)
    fp = open(reflection_json_path, 'r', encoding="utf-8")

    major_names = json.load(fp).keys()
    print("正在检索开课的所有院系\n--------------------------------------")
    for major_name in major_names:
        print(major_name)
        new_args = args
        new_args["major"] = major_name
        # 筛重
        temp_list = check_course_info(spider, new_args)
        for course in temp_list:
            if course.id not in [x.id for x in course_list]:
                course_list.append(course)

    return course_list
