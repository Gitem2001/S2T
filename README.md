# S2T System

S2T System — FastAPI приложение для преобразования русской речи в текст.


**Модель**:

vosk-model-small-ru-0.22 - официальная документация [documentation](https://alphacephei.com/vosk/), [github api](https://github.com/alphacep/vosk-api), 

В случае необходимость решения speech recognition на других языках возможна замена модели из доступных [models](https://alphacephei.com/vosk/models)

В случае необходимость запуска решения на локальных устройствах рекомендуется использование моделей small

Для серверной обработки возможно использование больших моделей

**Функции**

**Контракт**

| Метод | Эндпоинт          | Описание                                                                              |
| ----- | ----------------- | ------------------------------------------------------------------------------------- |
| POST  | /speech/recognize | Вернуть транскрибированный ответ в течении 3 секунд. <br> Иначе вернуть id задачи. |
| GET   | /speech/recognize | Получить результат обработки по id задачи.                                            |



**Примеры ответа**:

Ответ в случае превышения времени исполнения 3 сек.
```json
{
  'task_id': "d4da55e0-9bd9-4d6d-b706-1a9cddacec4c"
}

```

Ответ в случае получения результата по task_id или при обработки менее 3 секунд
```json
{
    "response": {
        "words": [
            {
                "startTime": "0.879999999s",
                "endTime": "1.159999992s",
                "word": "some"
            },
            {
                "startTime": "1.219999995s",
                "endTime": "1.539999988s",
                "word": "text"
            }
        ],
        "text": "some text"
    }
}
```

**Запуск приложения**

Для запуска приложения, установите все библиотеки из requirements.txt, после чего запустите fastapi приложение backend $\rightarrow$ controller $\rightarrow$ main.py 

В текущей версии приложения, не был реализован IO интерфейс. Для отладки работы API использовался файл data/audio_files/test.mp4
