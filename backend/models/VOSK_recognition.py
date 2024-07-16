import subprocess
from vosk import Model, KaldiRecognizer, SetLogLevel
import json
SAMPLE_RATE = 16000

SetLogLevel(-1)
def custom_SrtResult(rec, stream):  # переписанная кастомная функция, на основе метода KaldiRecognizer.SrtResult
    '''
    Функция для распознования речи на аудио, с использование VOSK API модели

    :param rec: KaldiReconginizer
    :param stream: Поток с открытым аудио файлом
    :return: json for with "words" - each word and start, end timestamp
                           "text" - final text
    '''
    results = []
    while True:
        data = stream.read(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            results.append(rec.Result())
    results.append(rec.FinalResult())

    words = []
    final_text = ''
    for res in results:
        jres = json.loads(res)
        if not "result" in jres:
            continue
        words.extend([{'start_time':x['start'],
                       'end_time': x['end'],
                       'word': x['word']} for x in jres['result']])
        final_text = ' '.join([final_text, jres['text']])

    return {'response':{
                        "words": words,
                        "text":final_text
                        }
            }



def recognition(file_path):
    model = Model(lang ='ru')  # возможно также использование встроенной модели в библиотеку lang=ru
                                                # в данном случае модель полностью работает локально path_model = 'vosk-model-small-ru-0.22'
                                                # в случае установки lang=ru произойдет автоматическая загрузка, но в первый раз понадобится сеть

    rec = KaldiRecognizer(model, SAMPLE_RATE)
    rec.SetWords(True)
    with subprocess.Popen(["ffmpeg", "-loglevel", "quiet", "-i",
                                file_path,
                                "-ar", str(SAMPLE_RATE) , "-ac", "1", "-f", "s16le", "-"],
                                stdout=subprocess.PIPE).stdout as stream:
        res = custom_SrtResult(rec, stream)
    return res

#recognition('/Users/rashidganeev/PycharmProjects/S2T_project/pythonProject/data/audio_files/test.mp4') #пример работы функции