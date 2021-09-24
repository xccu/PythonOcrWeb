# 需要安装：
#   fastapi     0.68.1
#   uvicorn     0.15.0

# API文档：http://127.0.0.1:8080/docs#

from fastapi import FastAPI
from ocr_vo import *
from ocr_service import *

app = FastAPI()

def startAPI():
    import uvicorn
    uvicorn.run(
        app=app,
        host="0.0.0.0",
        port=8080,
        workers=1)

@app.post('/recognize')
def recognize(request_data: RecognizeRequestVO):
    vo = RecognizeResponseVO()
    sercice = OcrService()
    results = sercice.recognize(request_data.path)
    # res = {"res": True}

    vo.path = request_data.path
    vo.data = results

    return vo

@app.get('/test/name={name}')
def test(name: str = None):
    return "hello "+name

