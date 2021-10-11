# 需要安装：
#   fastapi             0.68.1
#   uvicorn             0.15.0
#   python-multipart    0.0.5

# API文档：http://127.0.0.1:8080/docs#
from fastapi import FastAPI, File, UploadFile
from ocr_config import *
from ocr_vo import *
from ocr_service import *
from ocr_util import *
import ocr_global as glb
app = FastAPI()

def startAPI():
    import uvicorn
    uvicorn.run(
        app = app,
        host = get_cfg("Web","host"),
        port = int(get_cfg("Web","port")),
        workers = 1)

@app.post(path='/ocr/hub/local',tags=['paddleHub'],description='识别本地图片')
async def ocr_hub_local(request_data: RecognizeRequestVO):
    # 程序计时器启动
    timer_start()

    vo = HubResponseVO()
    sercice = HubService()
    results = sercice.recognize(request_data.path)

    # 程序计时器结束
    timer_end()

    # res = {"res": True}
    vo.file = request_data.path
    vo.data = results
    vo.time = timer_get()
    return vo

@app.post(path="/ocr/hub/",tags=['paddleHub'],description='识别上传的图片')
async def ocr_hub(fileb: UploadFile = File(...)):
    # 程序计时器启动
    timer_start()

    # 写文件 将获取的fileb文件内容，写入到新文件中
    await async_write_fileb(glb.g_upload_path + fileb.filename, fileb)
    #开始识别
    vo = HubResponseVO()
    sercice = HubService()
    results = sercice.recognize(glb.g_upload_path + fileb.filename)

    # 程序计时器结束
    timer_end()

    # res = {"res": True}
    vo.file = fileb.filename
    vo.snaps = results
    vo.time = timer_get()
    return vo

@app.post(path="/ocr/hub/snap",tags=['paddleHub'],description='分割并识别图片')
async def ocr_hub_snap(template:str='invoice.json',fileb: UploadFile = File(...)):
    # 程序计时器启动
    timer_start()
    # 写文件 将获取的fileb文件内容，写入到新文件中
    await async_write_fileb(glb.g_upload_path + fileb.filename, fileb)

    service = TemplateService()
    splits = service.split_image(fileb.filename,template)

    sercice = HubService()
    results = sercice.recognize_snap(splits)
    # 程序计时器结束
    timer_end()

    vo = HubSnapResponseVO()
    vo.file = fileb.filename
    vo.datas = results
    vo.time = timer_get()
    return vo

@app.post(path='/ocr/hub/detect',tags=['paddleHub'],description='检测文本位置')
async def ocr_hub_detect(fileb: UploadFile = File(...)):

    # 写文件 将获取的fileb文件内容，写入到新文件中
    await async_write_fileb(glb.g_upload_path + fileb.filename, fileb)

    timer_start()
    sercice = HubService()
    result =  sercice.detect_position(glb.g_upload_path + fileb.filename)
    timer_end()
    print(timer_get())

    return result

@app.post(path="/ocr",tags=['paddleOcr'],description='OCR识别上传的图片')
async def ocr(fileb: UploadFile = File(...)):
    # 程序计时器启动
    timer_start()

    # 写文件 将获取的fileb文件内容，写入到新文件中
    await async_write_fileb(glb.g_upload_path + fileb.filename, fileb)
    #开始识别
    vo = OcrResponseVO()
    sercice = OcrService()
    results = sercice.recognize(glb.g_upload_path + fileb.filename)

    # 程序计时器结束
    timer_end()

    vo.file = fileb.filename
    vo.datas = results
    vo.time = timer_get()
    return vo

@app.post(path="/ocr/snap",tags=['paddleOcr'],description='OCR识别上传的图片')
async def ocr_snap(template:str='invoice.json',fileb: UploadFile = File(...)):
    # 程序计时器启动
    timer_start()

    # 写文件 将获取的fileb文件内容，写入到新文件中
    await async_write_fileb(glb.g_upload_path + fileb.filename, fileb)
    service = TemplateService()
    snaps = service.split_image(fileb.filename, template)

    #开始识别
    vo = OcrSnapResponseVO()
    sercice = OcrService()
    results = sercice.recognize_snap(snaps)

    # 程序计时器结束
    timer_end()

    vo.file = fileb.filename
    vo.datas = results
    vo.time = timer_get()
    return vo

@app.delete(path='/clean',tags=['common'],description='清空临时文件夹')
def clean():
    arr= clean_folder(glb.g_upload_path)
    arr=arr+clean_folder(glb.g_temp_path)
    arr = arr + clean_folder(glb.g_ocr_result)
    return arr

@app.get('/test/name={name}',tags=['common'],description='测试')
def test(name: str = None):
    return name