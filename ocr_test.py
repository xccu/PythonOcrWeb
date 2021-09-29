import json

import  ocr_util
from ocr_service import TemplateService
from ocr_vo import *


if __name__ == '__main__':
    testStr = ocr_util.read('templates/template1.json')


    temp = json.loads(testStr)
    tempboxes = temp['boxes']
    boxes = []
    for box in tempboxes:
        boxes.append(box['position'])

    # 对象转Json
    # template = Template('模板')
    # box= Box('标题',[126, 148], [255, 148], [255, 182], [126, 182])
    # template.boxes.append(box)
    # box= Box('供货单位',[53, 183], [323, 183], [323, 218], [53, 218])
    # template.boxes.append(box)
    #
    # jsonstr = json.dumps(template, default=lambda x: x.__dict__,ensure_ascii=False,sort_keys=False, indent=2)
    # print(jsonstr)

    service =TemplateService()
    service.shot("D:\list2.jpg",boxes)
