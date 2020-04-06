import pytesseract
from PIL import Image
import requests
from function import common_functions
import function.function_utils as utils

target_url = "http://elite.nju.edu.cn/jiaowu/login.do"


def recognize_captcha(file_path):
    image = Image.open(file_path)
    # 灰度化
    gray = image.convert('L')
    # gray.show()
    data = gray.load()
    w, h = image.size
    for i in range(w):
        for j in range(h):
            if data[i, j] > 170:
                data[i, j] = 255
            else:
                data[i, j] = 0
    gray.show()
    result = pytesseract.image_to_string(gray)
    return result


def login(username, passwd, validcode):
    post_data = {'userName': username, 'password': passwd, 'returnUrl': 'null', 'ValidateCode': validcode}
    headers = {
        'Referer': "http://elite.nju.edu.cn/jiaowu/exit.do?type=student",
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
    request_cookie = {'JSESSIONID': "2CB8E419A90489CAA9081FC2D1EFB219", 'ARRAFFINITY': "80372ade9da56061dc1cfb0f216b6917726c2c01e3d804e60cad7fce0e0af662"}
    response = requests.post(url=target_url, data=post_data, headers=headers, cookies=request_cookie)

    response_cookies = response.cookies
    # print(cookies)
    return response_cookies


if __name__ == '__main__':
    """
    driver_path = "D:/myuniversity/我的项目/python/浏览器驱动/chromedriver.exe"
    index_save_path = "./data/index.png"
    captcha_save_path = "./data/captcha.png"
    webdriver = webdriver.Chrome(executable_path=driver_path)
    webdriver.get(target_url)
    # 取得验证码图片的位置和大小
    # 248,435
    pic = webdriver.find_element_by_id("ValidateImg")
    pic_loc = pic.location
    pic_size = pic.size
    webdriver.save_screenshot(index_save_path)
    print("截屏保存成功\n---------------------------")
    image = Image.open(index_save_path)
    # print(pic_loc)
    rec = (
        pic_loc["x"] + 52, pic_loc["y"] + 89, pic_loc["x"] + 50 + pic_size["width"],
        pic_loc["y"] + 89 + pic_size["height"])
    captcha = image.crop(rec)
    captcha.save(captcha_save_path)
    print("验证码保存成功\n----------------------------")
    
    # 识别验证码
    result = recognize_captcha(captcha_save_path)
    print(result)
    """
    cookie = {"JSESSIONID":"A920FFA968FA8073CD6A9D0781131CAA","ARRAffinity":"3f447fcc3aa80b67dadcb54645dd16f795e247520a46ddbe2d42786f3d88cf8e","user_id":"181250046 1586155451875"}
    spider = common_functions.LoginSpider(cookie)
    spider.start_session()
    spider.cancel_exam_only_application(course_id='00000041')
    print("任务结束")
