import configparser
import os

from distlib._backport import shutil


def read(file_path,encoding = 'utf-8'):
    with open(file_path, 'r', encoding=encoding) as f:
        return f.read()\

def write(file_path,data):
    with open(file_path, 'w') as f:
        f.write(data)

def write_bytes(file_path,data):
    with open(file_path, "wb") as f:
        f.write(data)

async def async_write_fileb(path,data):
    # 二进制流读取前端上传到的fileb文件
    contents = await data.read()
    # 写文件 将获取的fileb文件内容，写入到新文件中
    write_bytes(path + data.filename, contents)

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
