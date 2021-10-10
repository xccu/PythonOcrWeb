import json

import  ocr_util
from ocr_service import TemplateService
from ocr_vo import *


if __name__ == '__main__':

    # 图片二值化
    from PIL import Image

    img = Image.open('./file/list3.jpg')

    # 模式L”为灰色图像，它的每个像素用8个bit表示，0表示黑，255表示白，其他数字表示不同的灰度。
    gray_img = img.convert('L')
    #gray_img.save("./file/list3-1.jpg")

    # 自定义灰度界限，大于这个值为黑色，小于这个值为白色
    threshold = 150

    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)

    # 图片二值化
    binary_img = gray_img.point(table, '1')
    binary_img.save("./file/list3.jpg")


