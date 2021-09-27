import numpy as np
import cv2

def shot(path, dt_boxes):  # 应用于predict_det.py中,通过dt_boxes中获得的四个坐标点,裁剪出图像
    img = cv2.imread(path)
    boxes_len = len(dt_boxes)
    num = 0
    while 1:
        if (num < boxes_len):
            box = dt_boxes[num]
            tl = box[0] #左上
            tr = box[1] #右上
            br = box[2] #右下
            bl = box[3] #左下
            print("打印转换成功数据num =" + str(num))
            print("tl:" + str(tl), "tr:" + str(tr), "br:" + str(br), "bl:" + str(bl))
            print(tr[1], bl[1], tl[0], br[0])

            # crop = img[153:177,131:250] #测试
            crop = img[int(tr[1]):int(bl[1]), int(tl[0]):int(br[0])]
            cv2.imwrite("D:/screenshot/" + str(num) + ".jpg", crop)
            num = num + 1
        else:
            break

if __name__ == '__main__':

    # 左上,右上,右下,左下
    boxes=[]
    boxes.append([[126, 148], [255, 148], [255, 182], [126, 182]])
    boxes.append([[53, 183], [323, 183], [323, 218], [53, 218]])
    boxes.append([[170, 231], [291, 231], [291, 254], [170, 254]])
    boxes.append([[150, 254], [275, 254], [275, 275], [150, 275]])
    boxes.append([[150, 281], [318, 281], [318, 303], [150, 303]])
    boxes.append([[150, 314], [318, 314], [318, 335], [150, 335]])
    boxes.append([[150, 337], [308, 337], [308, 363], [150, 363]])
    boxes.append([[150, 368], [220, 368], [220, 390], [150, 390]])
    boxes.append([[155, 395], [220, 395], [220, 420], [155, 420]])
    boxes.append([[155, 425], [220, 425], [220, 450], [155, 450]])
    shot("D:\list2.jpg",boxes)
