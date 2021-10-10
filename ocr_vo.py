
from pydantic import BaseModel

#Ocr识别数据
class OcrData(BaseModel):
    text : str = None
    confidence : str = None
    position : str = None

class OcrSnapData(BaseModel):
    text : str = None
    confidence : str = None
    name : str = None

#Ocr截图
class OcrSnap(BaseModel):
    name: str = None
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
class HubResponseVO(BaseModel):
    file: str = None
    time: float = 0.0
    snaps: OcrSnap=[]

class HubSnapResponseVO(BaseModel):
    file: str = None
    time: float = 0.0
    datas: OcrSnapData=[]

class OcrResponseVO(BaseModel):
    file: str = None
    time: float = 0.0
    datas: OcrData=[]

class OcrSnapResponseVO(BaseModel):
    file: str = None
    time: float = 0.0
    datas: OcrSnapData=[]


