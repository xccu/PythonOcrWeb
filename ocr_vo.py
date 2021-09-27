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

class RecognizeRequestVO(BaseModel):
    path: str = None

class RecognizeResponseVO(BaseModel):
    file: str = None
    time: float = None
    snaps: OcrSnap=[]

