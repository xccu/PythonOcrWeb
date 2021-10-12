import yaml
import os

import ocr_config

if __name__ == '__main__':
    # 获取当前文件路径 D:/WorkSpace/StudyPractice/Python_Yaml/YamlStudy
    filePath = os.path.dirname(__file__)
    print(filePath)
    # 获取当前文件的Realpath  D:\WorkSpace\StudyPractice\Python_Yaml\YamlStudy\YamlDemo.py
    fileNamePath = os.path.split(os.path.realpath(__file__))[0]
    print(fileNamePath)
    # 获取配置文件的路径 D:/WorkSpace/StudyPractice/Python_Yaml/YamlStudy\config.yaml
    yamlPath = os.path.join(fileNamePath, 'config.yaml')
    print(yamlPath)
    # 加上 ,encoding='utf-8'，处理配置文件中含中文出现乱码的情况。
    f = open(yamlPath, 'r', encoding='utf-8')

    cont = f.read()

    x = yaml.load(cont)
    print(type(x))
    print(x)
    print(x['Web'])
    print(type(x['Web']))
    print(x['Web']['port'])
    print(type(x['Web']['host']))
    print(x['Ocr'])
    print(x['Ocr']['module'])
    print(x['Ocr']['useGpu'])
    print(x['Ocr']['output'])
    print(x['Ocr']['boxThresh'])
    print(x['Ocr']['textThresh'])

    print(x.get('Web').get('port'))

    print(type(x.get('Ocr')))



