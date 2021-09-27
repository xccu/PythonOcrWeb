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
from ocr_config import *

class OcrService():

    def __init__(self):
        self.text = []

        # 读取配置
        self.module = get_option("Ocr", "module")
        self.useGpu = bool(int(get_option("Ocr", "useGpu")))
        self.output = bool(int(get_option("Ocr", "output")))
        self.boxThresh = float(get_option("Ocr", "boxThresh"))
        self.textThresh = float(get_option("Ocr", "textThresh"))

        # chinese_ocr_db_crnn_mobile
        # chinese_ocr_db_crnn_server
        self.ocr = hub.Module(name=self.module)

    def recognize(self, data):

        np_images =None
        if type(data) == str:
            np_images =[cv2.imread(data)] #读取测试文件夹test.txt中的照片路径
        elif type(data) == list:
            np_images = data

        results = self.ocr.recognize_text(
            images=np_images,               #图片数据，ndarray.shape 为 [H, W, C]，BGR格式；
            use_gpu=self.useGpu,            #是否使用 GPU；若使用GPU，请先设置CUDA_VISIBLE_DEVICES环境变量
            output_dir='ocr_result',        #图片的保存路径，默认设为 ocr_result；
            visualization=self.output,      #是否将识别结果保存为图片文件；
            box_thresh=self.boxThresh,      #检测文本框置信度的阈值；（准确率）
            text_thresh=self.textThresh)    #识别中文文本置信度的阈值；（准确率）

        self.text = []
        snaps : OcrSnap = []
        for result in results:
            ocrDatas : OcrData = []
            snap =OcrSnap()
            snap.path=result['save_path']
            datas = result['data']
            for data in datas:
                ocrData = OcrData()
                ocrData.text = data['text']
                ocrData.confidence = data['confidence']
                ocrData.position = str(data['text_box_position'])
                self.text.append(str(data['text']))
                ocrDatas.append(ocrData)
            snap.datas = ocrDatas
            snaps.append(snap);
        return snaps

    def writeText(self, filename):
        with open(filename, 'w') as f:
            for i in self.text:
                f.write(str(i))