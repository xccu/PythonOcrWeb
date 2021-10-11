import configparser

import PIL
from fastapi import UploadFile
import os
import time
from PIL import Image
from distlib._backport import shutil

import ocr_global as glb


# 文件操作
def read(file_path,encoding = 'utf-8'):
    with open(file_path, 'r', encoding=encoding) as f:
        return f.read()

def write(file_path,data):
    with open(file_path, 'w') as f:
        f.write(data)

def write_bytes(file_path,data):
    with open(file_path, "wb") as f:
        f.write(data)

async def async_write_fileb(path,data:UploadFile):
    # 二进制流读取前端上传到的fileb文件
    contents = await data.read()
    # 写文件 将获取的fileb文件内容，写入到新文件中
    write_bytes(path, contents)

def clean_folder(folder_path):
    result = []
    del_list = os.listdir(folder_path)
    for f in del_list:
        file_path = os.path.join(folder_path, f)
        result.append(file_path)
        if os.path.isfile(file_path):
            os.remove(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    return result

# 计时器
def timer_start():
    glb.g_start = time.perf_counter()

def timer_end():
    glb.g_end = time.perf_counter()

def timer_get():
    span = glb.g_end - glb.g_start
    glb.g_end = 0.0
    glb.g_start = 0.0
    return span

# 图像处理

# PIL 纠正图像自动旋转
def img_correct_rotate(img):
    if not img:
        return img

    exif_orientation_tag = 274

    # Check for EXIF data (only present on some files)
    if hasattr(img, "_getexif") and isinstance(img._getexif(), dict) and exif_orientation_tag in img._getexif():
        exif_data = img._getexif()
        orientation = exif_data[exif_orientation_tag]

        # Handle EXIF Orientation
        if orientation == 1:
            # Normal image - nothing to do!
            pass
        elif orientation == 2:
            # Mirrored left to right
            img = img.transpose(PIL.Image.FLIP_LEFT_RIGHT)
        elif orientation == 3:
            # Rotated 180 degrees
            img = img.rotate(180)
        elif orientation == 4:
            # Mirrored top to bottom
            img = img.rotate(180).transpose(PIL.Image.FLIP_LEFT_RIGHT)
        elif orientation == 5:
            # Mirrored along top-left diagonal
            img = img.rotate(-90, expand=True).transpose(PIL.Image.FLIP_LEFT_RIGHT)
        elif orientation == 6:
            # Rotated 90 degrees
            img = img.rotate(-90, expand=True)
        elif orientation == 7:
            # Mirrored along top-right diagonal
            img = img.rotate(90, expand=True).transpose(PIL.Image.FLIP_LEFT_RIGHT)
        elif orientation == 8:
            # Rotated 270 degrees
            img = img.rotate(90, expand=True)

    return img

# 图片二值化
def img_binaryzation(path):

    img = Image.open(path)

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
    binary_img.save(path)

