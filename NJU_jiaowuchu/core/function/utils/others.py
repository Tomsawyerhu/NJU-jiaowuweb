import pytesseract as pytesseract
from PIL import Image


# 识别验证码
def recognize_captcha(file_path):
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
