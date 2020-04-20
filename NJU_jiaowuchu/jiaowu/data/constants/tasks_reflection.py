from jiaowu.core.function.download.download_functions import check_grades, get_timetable, crawl_news, check_course_info, \
    check_all_course_info
from jiaowu.core.function.statuschange.exit import terminate
from jiaowu.core.function.save.save_functions import save_as_excel
from jiaowu.core.function.statuschange.switchaccount import switch_account
from jiaowu.core.function.upload.upload_functions import apply_for_exam_only, cancel_exam_only_application

# 任务编号和对应的函数指针
TASK_LIST = {
    # DOWNLOAD
    "CHECK_GRADES": check_grades,
    "CHECK_TIMETABLE": get_timetable,
    'CHECK_CURRICULUM': check_course_info,
    'CHECK_ALL_CURRICULUM': check_all_course_info,
    "CHECK_NEWS": crawl_news,
    # UPLOAD
    "APPLY_FOR_EXAM_ONLY": apply_for_exam_only,
    "CANCEL_EXAM_ONLY": cancel_exam_only_application,
    "EXIT": terminate,
    "SAVE_AS_EXCEL": save_as_excel,
    "SWITCH_ACCOUNT": switch_account
}

# 参数简写及对应的参数名
PARAM_LIST = {
    'y': "year",
    't': "term",
    'g': 'grade',
    'm': 'major',
    'op': 'old_pwd',
    'np': 'new_pwd',
    'cn': 'course_name',
    'ci': 'course_id',
    'dt': 'data_type',
    'fp': 'file_path',
    'username': "username",
    'password': 'password',
}
