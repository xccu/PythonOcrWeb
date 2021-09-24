# 需要安装：
#   PaddleOCR       2.3.0.1
#   paddlepaddle    2.1.2
#   shapely         1.7.1
#   pyclipper       1.3.0

import os
os.environ['HUB_HOME'] = "./modules"
import cv2
import paddlehub as hub
from ocr_vo import *


class OcrService():

    def __init__(self):
        self.text = []
        self.ocr = hub.Module(name="chinese_ocr_db_crnn_server")

    def recognize(self, path):
        np_images =[cv2.imread(path)] #读取测试文件夹test.txt中的照片路径
        results = self.ocr.recognize_text(
            images=np_images,         #图片数据，ndarray.shape 为 [H, W, C]，BGR格式；
            use_gpu=False,            #是否使用 GPU；若使用GPU，请先设置CUDA_VISIBLE_DEVICES环境变量
            output_dir='ocr_result',  #图片的保存路径，默认设为 ocr_result；
            visualization=True,       #是否将识别结果保存为图片文件；
            box_thresh=0.5,           #检测文本框置信度的阈值；
            text_thresh=0.5)          #识别中文文本置信度的阈值；

        self.text = []
        ocrDatas: OcrData = []
        for result in results:
            data = result['data']
            save_path = result['save_path']
            for infomation in data:
                ocrData = OcrData()
                ocrData.text = infomation['text']
                ocrData.confidence = infomation['confidence']
                ocrData.position = str(infomation['text_box_position'])
                print('text: ', infomation['text'],
                      '\tconfidence: ', infomation['confidence'],
                      '\tposition: ', infomation['text_box_position'])
                self.text.append(str(infomation['text']))
                ocrDatas.append(ocrData)

        return ocrDatas

    def writeText(self, filename):
        with open(filename, 'w') as f:
            for i in self.text:
                f.write(str(i))