
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

class Box():
    def __init__(self, field, *position):
        self.field: str= field
        self.position: int = []
        self.position += position

class Template():
    def __init__(self, name, *boxes):
        self.name: str= name
        self.boxes: Box=[]
        self.boxes+= boxes


#http请求vo
class RecognizeRequestVO(BaseModel):
    path: str = None

#http响应vo
class RecognizeResponseVO(BaseModel):
    file: str = None
    time: float = None
    snaps: OcrSnap=[]

class OcrResponseVO(BaseModel):
    file: str = None
    time: float = None
    datas: OcrData=[]




