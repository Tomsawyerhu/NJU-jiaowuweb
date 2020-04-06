import re
import xlwt as xlwt
from xlwt import Font
from code.status_code import StatusCode as code


class TLparser:
    @staticmethod
    def parse(data):
        reflection = {"一": 1, "二": 2, "三": 3, "四": 4, "五": 5, "六": 6, "日": 7}
        pattern = re.compile("周([一二三四五六日]) 第(\d+)-(\d+)节 (\S+.*周) (.+)\n*")
        result = re.findall(pattern, data)
        all_arrangement = []
        if len(result) > 0:
            for sub_result in result:
                # 天
                day = reflection[sub_result[0]]
                # 时间段
                lesson = (int(sub_result[1]), int(sub_result[2]))
                # 周
                x = sub_result[3]
                week = ""
                if re.match("(\d+-\d+)周", x):
                    week = re.match("(\d+-\d+)周", x).group(1)
                elif x == '单周':
                    week = '单'
                elif x == '双周':
                    week = '双'
                else:
                    y = re.findall(re.compile("第(\d+)周"), x)
                    weeks = []
                    for z in y:
                        weeks.append(z)
                    week = ','.join(weeks)

                # 地点
                loc = sub_result[4].strip()
                all_arrangement.append((day, lesson, week, loc))
        return all_arrangement


class ClassInfoFormatter:
    def __init__(self, class_info):
        self.class_info = class_info

    def format(self):
        x = []
        class_name = self.class_info.name
        class_tl = self.class_info.time_and_loc
        class_tl_parse = TLparser.parse(class_tl)
        for ele in class_tl_parse:
            format_str = class_name + " " + ele[3] + "<" + ele[2] + ">"
            x.append((format_str, ele[0], ele[1]))
        return x


def save_timetable_as_excel(data, file_path):
    info_list = []
    for course_info in data:
        formatter = ClassInfoFormatter(course_info)
        format_data = formatter.format()
        for x in format_data:
            info_list.append(x)
    try:
        li = ['', '一', '二', '三', '四', '五']
        workbook = xlwt.Workbook(encoding='utf-8')
        sheet = workbook.add_sheet("课程表")

        # 单元格文字居中
        style = xlwt.XFStyle
        al = xlwt.Alignment()
        al.horz = 0x02  # 设置水平居中
        al.vert = 0x01  # 设置垂直居中
        style.alignment = al
        fnt = Font()  # 创建一个文本格式，包括字体、字号和颜色样式特性
        fnt.name = u'微软雅黑'  # 设置其字体为微软雅黑
        style.font = fnt
        style.num_format_str = 'yyyy-mm-dd'  # 日期格式
        style.borders = xlwt.Formatting.Borders()
        style.pattern = xlwt.Formatting.Pattern()
        style.protection = xlwt.Formatting.Protection()

        for i in range(6):
            sheet.write(0, i, li[i], style=style)
        for i in range(1, 12):
            sheet.write(i, 0, str(i), style=style)
        flags = [-1] * len(info_list)
        corporated_info_list = []
        for y in range(len(info_list)):
            # 先做一遍遍历，将相同时间段的课程信息合并
            if flags[y] < 0:
                corporated_info = info_list[y][0]
                for j in range(y + 1, len(info_list)):
                    if flags[j] < 0 and info_list[j][1] == info_list[y][1] and info_list[j][2] == info_list[y][2]:
                        flags[j] = 0
                        corporated_info += "\n" + info_list[j][0]
                flags[y] = 0
                corporated_info_list.append((corporated_info, info_list[y][1], info_list[y][2]))
        for x in corporated_info_list:
            sheet.write_merge(x[2][0], x[2][1], x[1], x[1], x[0], style=style)
        # 设置单元格格式
        for i in range(1, 6):
            col = sheet.col(i)
            col.width = 256 * 35
            col.height = 256 * 25

        workbook.save(file_path)

    except Exception as e:
        print(e)
        print(code.CANNOT_SAVE_AS_EXCEL.get_msg())


# def save_timetable_as_pdf(data,file_path):

if __name__ == '__main__':
    s = "周三 第5-6节 双周 仙Ⅱ-503\n周一 第3-4节 1-17周 仙Ⅱ-503\n周一 第9-10节 1-17周 基础实验楼丙区513\n"
    d = TLparser.parse(s)
    print(0)
