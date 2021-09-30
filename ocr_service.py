# 需要安装：
#   PaddleOCR       2.3.0.1
#   paddlepaddle    2.1.2
#   shapely         1.7.1
#   pyclipper       1.3.0
import json
import os

import ocr_util

os.environ['HUB_HOME'] = "./modules"
import cv2
import paddlehub as hub
from ocr_vo import *
from ocr_config import *

# Ocr识别类
class OcrService():

    def __init__(self):
        self.text = []

        # 读取配置
        self.module = get_option("Ocr", "module")
        self.use_gpu = bool(int(get_option("Ocr", "useGpu")))
        self.output = bool(int(get_option("Ocr", "output")))
        self.box_thresh = float(get_option("Ocr", "boxThresh"))
        self.text_thresh = float(get_option("Ocr", "textThresh"))

        # chinese_ocr_db_crnn_mobile
        # chinese_ocr_db_crnn_server
        self.ocr = hub.Module(name=self.module)

    def detect_position(self, data):
        np_images = None
        if type(data) == str:
            np_images = [cv2.imread(data)]  # 读取测试文件夹test.txt中的照片路径
        elif type(data) == list:
            np_images = data

        detection_results=self.ocr.text_detector_module.detect_text(
            images=np_images,
            use_gpu=self.use_gpu,
            box_thresh=self.box_thresh)  #探测文本的位置

        return detection_results

    def recognize(self, data):

        np_images =None
        if type(data) == str:
            np_images =[cv2.imread(data)] #读取测试文件夹test.txt中的照片路径
        elif type(data) == list:
            np_images = data

        results = self.ocr.recognize_text(
            images=np_images,               #图片数据，ndarray.shape 为 [H, W, C]，BGR格式；
            use_gpu=self.use_gpu,           #是否使用 GPU；若使用GPU，请先设置CUDA_VISIBLE_DEVICES环境变量
            output_dir='ocr_result',        #图片的保存路径，默认设为 ocr_result；
            visualization=self.output,      #是否将识别结果保存为图片文件；
            box_thresh=self.box_thresh,      #检测文本框置信度的阈值；（准确率）
            text_thresh=self.text_thresh)    #识别中文文本置信度的阈值；（准确率）

        self.text = []
        snaps : OcrSnap = []
        for result in results:
            ocr_datas : OcrData = []
            snap =OcrSnap()
            snap.path=result['save_path']
            datas = result['data']
            for data in datas:
                ocr_data = OcrData()
                ocr_data.text = data['text']
                ocr_data.confidence = data['confidence']
                ocr_data.position = str(data['text_box_position'])
                self.text.append(str(data['text']))
                ocr_datas.append(ocr_data)
            snap.datas = ocr_datas
            snaps.append(snap);
        return snaps

    def writeText(self, filename):
        with open(filename, 'w') as f:
            for i in self.text:
                f.write(str(i))

# 模板处理类
class TemplateService():
    def __init__(self,img_root = './file/',template_root='./templates/'):
        self.img_root= img_root
        self.template_root=template_root

    def split_image(self,file_name,template):
        # 从json中读取模板信息
        json_str = ocr_util.read(self.template_root+template)

        temp = json.loads(json_str)
        boxes = temp['boxes']

        return self.shot(file_name, boxes)

    # 通过boxes中获得的四个坐标点,裁剪出图像
    def shot(self,file_name,boxes):

        text = []
        img = cv2.imread(self.img_root+file_name)
        boxes_len = len(boxes)
        num = 0

        while (num < boxes_len):
            box = boxes[num]
            tl = box['position'][0]  # 左上
            tr = box['position'][1]  # 右上
            br = box['position'][2]  # 右下
            bl = box['position'][3]  # 左下
            print(tr[1], bl[1], tl[0], br[0])

            # crop = img[153:177,131:250] #测试
            crop = img[int(tr[1]):int(bl[1]), int(tl[0]):int(br[0])]
            text.append("./temp/{}-{}-{}".format(str(num),box['field'],file_name))
            # cv2.imwrite("./temp/{}-{}-{}".format(str(num),box['field'],file_name), crop)
            cv2.imencode('.jpg', crop)[1].tofile("./temp/{}-{}-{}".format(str(num),box['field'],file_name))
            num = num + 1
        return text
