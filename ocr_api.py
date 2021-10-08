# 需要安装：
#   fastapi             0.68.1
#   uvicorn             0.15.0
#   python-multipart    0.0.5

# API文档：http://127.0.0.1:8080/docs#
import ocr_util
from ocr_config import *
from fastapi import FastAPI, File, UploadFile
# from starlette.responses import FileResponse
from ocr_vo import *
from ocr_service import *
from ocr_util import *

#计时所需要的时间库
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

    # 程序计时器启动
    start = time.perf_counter()

    vo = RecognizeResponseVO()
    sercice = OcrService()
    results = sercice.recognize(request_data.path)

    # 程序计时器结束
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
    # 写文件 将获取的fileb文件内容，写入到新文件中
    ocr_util.async_write_fileb("./file/" + fileb.filename, fileb)
    #开始识别
    vo = RecognizeResponseVO()
    sercice = OcrService()
    results = sercice.recognize("./file/" + fileb.filename)

    # 程序计时器结束
    end = time.perf_counter()

    # res = {"res": True}
    vo.file = fileb.filename
    vo.snaps = results
    vo.time = end-start
    return vo


@app.post("/split")
async def split_recognize(fileb: UploadFile = File(...)):
    # 程序计时器启动
    start = time.perf_counter()
    # 写文件 将获取的fileb文件内容，写入到新文件中
    ocr_util.async_write_fileb("./file/" + fileb.filename, fileb)

    service = TemplateService()
    splits = service.split_image(fileb.filename,'template1.json')

    np_images = [cv2.imread(image_path) for image_path in splits]
    sercice = OcrService()
    results = sercice.recognize(np_images)
    # 程序计时器结束
    end = time.perf_counter()

    vo = RecognizeResponseVO()
    vo.file = fileb.filename
    vo.snaps = results
    vo.time = end-start
    return vo

@app.post('/detect')
def detect(fileb: UploadFile = File(...)):
    # 写文件 将获取的fileb文件内容，写入到新文件中
    ocr_util.async_write_fileb("./file/" + fileb.filename, fileb)

    start = time.perf_counter()
    sercice = OcrService()
    result =  sercice.detect_position("./file/" + fileb.filename)
    end = time.perf_counter()
    print(end-start)

    return result

@app.delete('/clean')
def clean():
    return ocr_util.clean_folder('./temp')

@app.get('/test/name={name}')
def test(name: str = None):
    return name

