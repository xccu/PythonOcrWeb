from pydantic import BaseModel

class OcrData(BaseModel):
    text : str = None
    confidence : str = None
    position : str=None

class RecognizeRequestVO(BaseModel):
    path: str = None

class RecognizeResponseVO(BaseModel):
    file: str = None
    time: float = None
    data: OcrData=[]

