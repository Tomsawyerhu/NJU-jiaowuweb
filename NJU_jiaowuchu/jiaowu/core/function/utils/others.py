import os
import re

import pytesseract as pytesseract
from PIL import Image

# 识别验证码
from scrapy import Selector

from jiaowu.core.function.utils.writer import JSONWriter
from jiaowu.core.model.spider_model import LoginSpider


def recognize_captcha(file_path):
    image = Image.open(file_path)
    # print(image.size)
    image = image.crop((1, 1, 70, 19))
    # 灰度化
    gray = image.convert('L')
    # gray.show()
    data = gray.load()
    w, h = image.size
    for i in range(w):
        for j in range(h):
            if data[i, j] > 129:
                data[i, j] = 255
            else:
                data[i, j] = 0
    # gray.show()
    result = pytesseract.image_to_string(gray)
    result = ''.join([x for x in list(result) if x != ' '])
    return result


def get_values(args, keys):
    # 从参数列表中获取参数
    for key in keys:
        if key in args.keys():
            yield args[key]
        else:
            yield None


def crawl_speciality_select(spider: LoginSpider):
    # 爬取院系对应的编号
    # **273%金融工程((
    # A41%*外国语言文学类((
    reflection_table = {}
    spider.update_header("Pragma", "no-cache")
    response = spider.task.get(
        url="http://elite.nju.edu.cn/jiaowu/student/teachinginfo/allCourseList.do?method=getTermAcademy")
    pattern1 = re.compile("\*\*(\d\d\d)%([\u4e00-\u9fa5a-zA-Z0-9()]+)\(\(")
    pattern2 = re.compile("(\S\S\S)%\*([\u4e00-\u9fa5a-zA-Z0-9()]+)\(\(")
    reflections1 = re.findall(pattern1, response.text)
    reflections2 = re.findall(pattern2, response.text)
    for reflection in reflections1:
        reflection_table[reflection[1]] = reflection[0]
    for reflection in reflections2:
        reflection_table[reflection[1]] = reflection[0]

    # todo 硬编码需修改
    json_writer = JSONWriter()
    curPath = os.path.abspath(os.path.dirname(__file__))
    paths_part = curPath.split('\\')
    for i in range(3):
        paths_part.pop()
    rootPath = '\\'.join(paths_part)
    print(rootPath)
    json_writer.write(reflection_table, rootPath + "\\data\\output\\major_reflection.json")
    print("一共有%d个专业" % (len(reflections1) + len(reflections2)))


def crawl_renew_course_id_reflection(spider: LoginSpider):
    # 爬取补选课程对应的编号
    # 导学，研讨，通识
    crawl_renew_discuss_and_public_id_reflection(spider, 1)
    # 经典悦读
    crawl_renew_read_id_reflection(spider)
    # 公选
    crawl_renew_discuss_and_public_id_reflection(spider, -1)
    # 跨专业
    pass
    # 通修
    pass


def crawl_renew_discuss_and_public_id_reflection(spider: LoginSpider, type):
    # 导学，研讨，通识 or 公选
    url = ""
    if type > 0:
        # 导学，研讨，通识
        url = "http://elite.nju.edu.cn/jiaowu/student/elective/courseList.do?method=discussRenewCourseList"
    else:
        url = "http://elite.nju.edu.cn/jiaowu/student/elective/courseList.do?method=publicRenewCourseList"
    pattern = re.compile("javascript:showCourseDetailInfo\((\d+),'(\d+)'\)")
    # 仙林校区
    xianlin_course_list = {}
    url1 = url + "&campus=仙林校区"
    response1 = spider.task.get(url=url1)
    selector1 = Selector(text=response1.text)
    course_selectors1 = selector1.xpath("//tr[@class='TABLE_TR_01']") + selector1.xpath("//tr[@class='TABLE_TR_02']")
    for selector in course_selectors1:
        tds = selector.xpath("./td")
        course_name = tds[2].xpath("./text()").get().strip()
        course_id = tds[9].xpath("./input/@value").get()
        if course_id is not None:
            xianlin_course_list[course_name] = course_id.strip()
    # 鼓楼校区
    gulou_course_list = {}
    url2 = url + "&campus=鼓楼校区"
    response2 = spider.task.get(url=url2)
    selector2 = Selector(text=response2.text)
    course_selectors2 = selector2.xpath("//tr[@class='TABLE_TR_01']") + selector2.xpath("//tr[@class='TABLE_TR_02']")
    for selector in course_selectors2:
        tds = selector.xpath("./td")
        course_name = tds[2].xpath("./text()").get().strip()
        course_id = re.match(pattern, tds[0].xpath("./a/@href")[0].get().strip()).group(1)
        gulou_course_list[course_name] = course_id

    # todo 硬编码需修改
    json_writer = JSONWriter()
    curPath = os.path.abspath(os.path.dirname(__file__))
    paths_part = curPath.split('\\')
    for i in range(3):
        paths_part.pop()
    rootPath = '\\'.join(paths_part)
    if type > 0:
        json_writer.write(xianlin_course_list, rootPath + "\\data\\output\\renew_discuss_xainlin.json")
        json_writer.write(gulou_course_list, rootPath + "\\data\\output\\renew_discuss_gulou.json")
    else:
        json_writer.write(xianlin_course_list, rootPath + "\\data\\output\\renew_public_xainlin.json")
        json_writer.write(gulou_course_list, rootPath + "\\data\\output\\renew_public_gulou.json")


def crawl_renew_read_id_reflection(spider: LoginSpider):
    # 经典悦读
    read_table = {}
    url = "http://elite.nju.edu.cn/jiaowu/student/elective/courseList.do"
    data = {'method': 'readRenewCourseList', 'type': 7}
    spider.update_header("Referer", "http://elite.nju.edu.cn/jiaowu/student/elective/readRenewCourseList.do?type=1")
    spider.update_header("X-Requested-With", "XMLHttpRequest")
    spider.update_header("X-Prototype-Version", "1.5.1")
    response = spider.task.post(url=url, data=data)
    selector = Selector(text=response.text)
    trs = selector.xpath("//table[@id='tbCourseList']/tbody/tr")
    pattern = re.compile("javascript:readRenewSelect\(event, '(\d+)'\)")
    for tr in trs:
        name = tr.xpath("./td")[1].xpath("./text()").get().strip()
        onclick_attr = tr.xpath("./td")[6].xpath("./@onclick").get()
        if onclick_attr is not None:
            id = re.match(pattern, onclick_attr).group(1)
            read_table[name] = id

        # todo 硬编码需修改
    json_writer = JSONWriter()
    curPath = os.path.abspath(os.path.dirname(__file__))
    paths_part = curPath.split('\\')
    for i in range(3):
        paths_part.pop()
    rootPath = '\\'.join(paths_part)
    json_writer.write(read_table, rootPath + "\\data\\output\\renew_read_all.json")


def crawl_renew_open_id_reflection(spider: LoginSpider):
    # todo
    # 跨专业
    open_table = {}
    url = "http://elite.nju.edu.cn/jiaowu/student/elective/courseList.do"
