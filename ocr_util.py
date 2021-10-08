import configparser
from fastapi import UploadFile
import os
import time

from distlib._backport import shutil

import ocr_global

#文件操作
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

#计时器
def timer_start():
    ocr_global.start = time.perf_counter()

def timer_end():
    ocr_global.end = time.perf_counter()

def timer_get():
    span = ocr_global.end - ocr_global.start
    ocr_global.end = 0.0
    ocr_global.start = 0.0
    return span