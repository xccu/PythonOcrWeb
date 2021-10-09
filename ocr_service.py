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
from paddleocr import PaddleOCR, draw_ocr

# PaddleHub识别类
class HubService():

    def __init__(self):
        self.text = []

        # 读取配置
        self.module = get_cfg("Ocr", "module")
        self.use_gpu = bool(int(get_cfg("Ocr", "useGpu")))
        self.output = bool(int(get_cfg("Ocr", "output")))
        self.box_thresh = float(get_cfg("Ocr", "boxThresh"))
        self.text_thresh = float(get_cfg("Ocr", "textThresh"))

        # chinese_ocr_db_crnn_mobile
        # chinese_ocr_db_crnn_server
        self.ocr = hub.Module(name=self.module)

    def detect_position(self, path):
        np_images = None
        if type(path) == str:
            np_images = [cv2.imread(path)]  # 读取测试文件夹test.txt中的照片路径
        elif type(path) == list:
            np_images = path

        detection_results=self.ocr.text_detector_module.detect_text(
            images=np_images,
            use_gpu=self.use_gpu,
            box_thresh=self.box_thresh)  #探测文本的位置

        return detection_results

    def recognize(self, path):
        np_images =None
        if type(path) == str:
            np_images =[cv2.imread(path)] #读取测试文件夹test.txt中的照片路径
        elif type(path) == list:
            np_images = [cv2.imread(image_path) for image_path in path]

        results = self.ocr.recognize_text(
            images=np_images,               #图片数据，ndarray.shape 为 [H, W, C]，BGR格式；
            use_gpu=self.use_gpu,           #是否使用 GPU；若使用GPU，请先设置CUDA_VISIBLE_DEVICES环境变量
            output_dir='ocr_result',        #图片的保存路径，默认设为 ocr_result；
            visualization=self.output,      #是否将识别结果保存为图片文件；
            box_thresh=self.box_thresh,     #检测文本框置信度的阈值；（准确率）
            text_thresh=self.text_thresh)   #识别中文文本置信度的阈值；（准确率）

        self.text = []
        snaps : OcrSnap = []
        i=0
        for result in results:
            ocr_datas : OcrData = []
            snap =OcrSnap()
            if type(path) == list:
                snap.name = path[i]
                i+=1
            else:
                snap.name = path
            for data in result['data']:
                ocr_data = OcrData()
                ocr_data.text = data['text']
                ocr_data.confidence = data['confidence']
                ocr_data.position = str(data['text_box_position'])
                self.text.append(str(data['text']))
                ocr_datas.append(ocr_data)
            snap.datas = ocr_datas
            snaps.append(snap);
        return snaps

    # 结果写文本
    def write_text(self, filename):
        with open(filename, 'w') as f:
            for i in self.text:
                f.write(str(i))

# paddleOcr识别类
class OcrService():
    def __init__(self):
        self.datas = []
        self.text = []
        # 读取配置
        self.ocr = PaddleOCR(
            use_angle_cls=True,
            use_gpu=bool(int(get_cfg("Ocr", "useGpu")))
        )

        self.module = get_cfg("Ocr", "module")
        self.use_gpu = bool(int(get_cfg("Ocr", "useGpu")))
        self.output = bool(int(get_cfg("Ocr", "output")))
        self.box_thresh = float(get_cfg("Ocr", "boxThresh"))
        self.text_thresh = float(get_cfg("Ocr", "textThresh"))

    def recognize(self, img_path):
        self.text = []
        ocr_datas: OcrData = []
        self.datas = self.ocr.ocr(img_path, cls=True)
        for data in self.datas:
            ocr_data = OcrData()
            ocr_data.text = str(data[1][0])
            ocr_data.confidence = str(data[1][1])
            ocr_data.position = str(data[0])
            ocr_datas.append(ocr_data)
            self.text.append(str(data[1][0]))

        if self.output:
            self.write_img(img_path)

        return ocr_datas

    # 结果写文本
    def write_text(self, filename):
        with open(filename, 'w') as f:
            for i in self.text:
                f.write(str(i))

    # 输出结果图片
    def write_img(self,img_path):
        from PIL import Image

        image = Image.open(img_path)
        image = ocr_util.correct_rotate(image) #纠正自动旋转
        boxes = [data[0] for data in self.datas]
        txts = [data[1][0] for data in self.datas]
        scores = [data[1][1] for data in self.datas]
        im_show = draw_ocr(image, boxes, txts, scores)
        im_show = Image.fromarray(im_show)
        im_show.save('result.jpg')  # 结果图片保存在代码同级文件夹中。


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

