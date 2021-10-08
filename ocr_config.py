import configparser
import os

path='config.ini'
cfg = configparser.ConfigParser()

def get_sections():
    cfg.read(path)  # 读取配置文件，如果写文件的绝对路径，就可以不用os模块
    return cfg.sections()

def get_cfg(section, option):
    cfg.read(path)  # 读取配置文件，如果写文件的绝对路径，就可以不用os模块
    return cfg.get(section, option)

def set_cfg(section, option, value):
    cfg.set(section, option, value)
    with open(path, "w+") as f:
        cfg.write(f)
