from pydantic import BaseModel

#Ocr识别数据
class OcrData(BaseModel):
    text : str = None
    confidence : str = None
    position : str=None

#Ocr截图
class OcrSnap(BaseModel):
    path: str = None
    datas: OcrData=[]

#http请求vo
class RecognizeRequestVO(BaseModel):
    path: str = None

#http响应vo
class RecognizeResponseVO(BaseModel):
    file: str = None
    time: float = None
    snaps: OcrSnap=[]

class Box():
    title: str=None
    position: int=[[]]

class Template():
    name: str=None
    boxes: Box=[]



