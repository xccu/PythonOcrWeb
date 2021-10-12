# 需要安装：
#   pyyaml      5.4.1

import configparser
import os
import yaml

fileNamePath = os.path.split(os.path.realpath(__file__))[0]
yamlPath = os.path.join(fileNamePath, 'config.yaml')

# 参考：https://www.cnblogs.com/klb561/p/10085328.html
def get_yaml(dict:str):
    f = open(yamlPath, 'r', encoding='utf-8')
    cont = f.read()
    x = yaml.load(cont)
    arr=dict.split('.')
    for item in arr:
        x=x.get(item)
    return x

path='config.ini'
cfg = configparser.ConfigParser()

def get_ini_sections():
    cfg.read(path)  # 读取配置文件，如果写文件的绝对路径，就可以不用os模块
    return cfg.sections()

def get_ini(section, option):
    cfg.read(path)  # 读取配置文件，如果写文件的绝对路径，就可以不用os模块
    return cfg.get(section, option)

def set_ini(section, option, value):
    cfg.set(section, option, value)
    with open(path, "w+") as f:
        cfg.write(f)
