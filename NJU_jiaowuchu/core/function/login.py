import pytesseract
from PIL import Image
import requests
from core.function import common_functions


# 识别验证码
def _recognize_captcha(file_path):
    image = Image.open(file_path)
    print(image.size)
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
    gray.show()
    result = pytesseract.image_to_string(gray)
    result = ''.join([x for x in list(result) if x != ' '])
    return result


# 登录
def _login(username, passwd, captcha, cookie):
    target_url = "http://elite.nju.edu.cn/jiaowu/login.do"
    post_data = {'userName': username, 'password': passwd, 'returnUrl': 'null', 'ValidateCode': captcha}
    headers = {
        'Referer': "http://elite.nju.edu.cn/jiaowu/",
        'Cache-Control': "max-age=0",
        'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        'Accept-Language': "zh-CN",
        'Content-Type': "application/x-www-form-urlencoded",
        'Upgrade-Insecure-Requests': "1",
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18362",
        'Accept-Encoding': "gzip, deflate",
        'Host': "elite.nju.edu.cn",
        'Connection': "keep-alive"
    }
    response = requests.post(url=target_url, data=post_data, headers=headers, cookies=cookie)
    response_cookies = response.cookies
    # print(cookies)
    return response_cookies


# 获取验证码response
def _get_validate_code_response():
    response = requests.get(url="http://elite.nju.edu.cn/jiaowu/ValidateCode.jsp")
    return response


def start_session(username, passwd):
    # 由于识别正确率低，暂时用循环的方法直到识别正确
    cookies=None
    while True:
        # 完整的获取验证码登录过程
        response = _get_validate_code_response()
        cookies1 = response.cookies
        cookies1_dict = requests.utils.dict_from_cookiejar(cookies1)
        captcha_save_path = "./data/raw_captcha.png"
        with open("./data/raw_captcha.png", "wb") as f:
            f.write(response.content)
        # 识别验证码
        result = _recognize_captcha(captcha_save_path)
        # print(result)
        cookies2 = _login(username, passwd, result, cookies1)
        cookies2_dict = requests.utils.dict_from_cookiejar(cookies2)

        # 识别正确
        if len(cookies2_dict)>0:
            # 合并cookie
            cookies_dict = dict(cookies1_dict, **cookies2_dict)
            cookies = requests.utils.cookiejar_from_dict(cookies_dict, cookiejar=None, overwrite=True)
            break
    return cookies


if __name__ == '__main__':
    cookie = start_session("181250046", "Hhc85851765")
    spider = common_functions.LoginSpider(cookie)
    spider.start_task()
    spider.cancel_exam_only_application(course_id='00000041')

    print("任务结束")
