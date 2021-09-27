from pydantic import BaseModel

class OcrData(BaseModel):
    text : str = None
    confidence : str = None
    position : str=None

class OcrInfo(BaseModel):
    path: str = None
    data: OcrData=[]

class RecognizeRequestVO(BaseModel):
    path: str = None

class RecognizeResponseVO(BaseModel):
    file: str = None
    time: float = None
    info: OcrInfo=[]

