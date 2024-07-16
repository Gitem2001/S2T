import uuid

from fastapi import FastAPI, BackgroundTasks
from backend.models.VOSK_recognition import recognition
from uuid import uuid4
import json
import asyncio
import uvicorn

#from fastapi import File, UploadFile, HTTPException
#from fastapi.responses import HTMLResponse, FileResponse
#import os
#from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Директория для хранения аудиофайлов
# AUDIO_DIRECTORY = "data/audio_files"
# HTML_DIRECTORY = "frontend/pages"

# app.mount("/static", StaticFiles(directory=HTML_DIRECTORY), name="static")
#
# if not os.path.exists(AUDIO_DIRECTORY):
#     os.makedirs(AUDIO_DIRECTORY)

STATIC_AUDIO_FILE_PATH = '/data/audio_files/test.mp4'
@app.get('/speech/recognize')
async def recognize():
    '''
    get запрос для запуска обработки файла
    return: В случае исполнения менее 3 сек json с результатом обработки
            В случае исполнения более 3 сек json с task id
    '''
    task_id = uuid4()
    try:
        result = await asyncio.wait_for(get_model_inference(task_id), timeout=3)
        return result
    except asyncio.TimeoutError:
        return {"task_id": task_id}

async def get_model_inference(task_id: uuid.UUID):
    '''
    Функция запуска инференса модели
    :param task_id: id задачи на обработку речи
    :return: json с результатом обработки
    '''
    print('Start model inference', task_id)
    res = recognition(STATIC_AUDIO_FILE_PATH)
    with open(f"data/results/{task_id}.json", "w") as outfile:
        print(res)
        json.dump(res, outfile)
    return res

@app.post('/speech/recognize/{task_id}')
async def get_res(task_id: uuid.UUID):
    '''
        post запрос для получения файла обработки
        :param task_id:  id задачи полученной с get запроса
        return: json с результатом обработки
        '''
    with open(f"data/results/{task_id}.json", "r") as file:
        return json.load(file)


# @app.get("/", response_class=HTMLResponse)
# async def read_root():
#     with open(os.path.join(HTML_DIRECTORY, "main.html")) as html_file:
#         return HTMLResponse(content=html_file.read())

# @app.post("/upload/")
# async def upload_audio(file: UploadFile = File(...)):
#     file_path = os.path.join(AUDIO_DIRECTORY, file.filename)
#     with open(file_path, "wb") as audio_file:
#         audio_file.write(file.file.read())
#     return {"filename": file.filename}
#
# @app.get("/download/{file_name}")
# async def download_audio(file_name: str):
#     file_path = os.path.join(AUDIO_DIRECTORY, file_name)
#     if os.path.exists(file_path):
#         return FileResponse(file_path, media_type='audio/mpeg', filename=file_name)
#     else:
#         raise HTTPException(status_code=404, detail="File not found")
#
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)