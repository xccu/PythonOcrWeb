# 需要安装：
#   fastapi             0.68.1
#   uvicorn             0.15.0
#   python-multipart    0.0.5

# API文档：http://127.0.0.1:8080/docs#

from ocr_config import *
from fastapi import FastAPI, File, UploadFile
# from starlette.responses import FileResponse
from ocr_vo import *
from ocr_service import *

#计时所需要的时间库
import datetime
import time

app = FastAPI()

def startAPI():

    import uvicorn
    uvicorn.run(
        app = app,
        host = get_option("Web","host"),
        port = int(get_option("Web","port")),
        workers = 1)

@app.post('/recognize/local')
async def recognize_local(request_data: RecognizeRequestVO):

    # 程序计时器，启动计时器
    start = time.perf_counter()

    vo = RecognizeResponseVO()
    sercice = OcrService()
    results = sercice.recognize(request_data.path)

    # 计算启动时间和结束时间的时间差
    end = time.perf_counter()

    # res = {"res": True}
    vo.file = request_data.path
    vo.data = results
    vo.time = end-start
    return vo

@app.post("/recognize")
async def recognize(fileb: UploadFile = File(...)):

    # 程序计时器启动
    start = time.perf_counter()
    # 二进制流读取前端上传到的fileb文件
    contents = await fileb.read()
    # 写文件 将获取的fileb文件内容，写入到新文件中
    with open("./file/" + fileb.filename, "wb") as f:
        f.write(contents)
    #开始识别
    vo = RecognizeResponseVO()
    sercice = OcrService()
    results = sercice.recognize("./file/" + fileb.filename)

    # 计算启动时间和结束时间的时间差
    end = time.perf_counter()

    # res = {"res": True}
    vo.file = fileb.filename
    vo.data = results
    vo.time = end-start
    return vo

@app.get('/test/name={name}')
def test(name: str = None):
    return "hello "+name

