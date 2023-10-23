import math
import numpy as np
import urllib3
import json
import base64
from pydub import AudioSegment


## mp3 파일을 pcm 파일로
def mp32pcm():
  audio_file_path = "./static/hello_preprocessing.mp3"
  pcm_file_path = "./static/hello.pcm"

  audio = AudioSegment.from_file(audio_file_path, format="mp3")
  audio = audio.set_sample_width(2)
  audio.export(pcm_file_path, format="s16le")

  return pcm_file_path


## api를 이용한 발음평가
def pronunciation_assessment(pcm_file_path, accessKey, script):
  openApiURL = "http://aiopen.etri.re.kr:8000/WiseASR/PronunciationKor" # 한국어
  languageCode = "korean"
  accessKey = accessKey 
  file = open(pcm_file_path, "rb")
  audioContents = base64.b64encode(file.read()).decode("utf8")
  file.close()

  requestJson = {
      "argument": {
          "language_code": languageCode,
          "script": script,
          "audio": audioContents
      }
  }

  http = urllib3.PoolManager()
  response = http.request(
      "POST",
      openApiURL,
      headers={"Content-Type": "application/json; charset=UTF-8","Authorization": accessKey},
      body=json.dumps(requestJson)
  )
  
  data = json.loads(response.data)
  score = data["return_object"]["score"]

  return score


def convert_score(score):
  score = 100 - (score - 1) * 25
  return math.floor(score)

pcm_file_path = mp32pcm()
print(pcm_file_path)

score = pronunciation_assessment(pcm_file_path, '17c34f27-babf-4fb7-8353-11dd5f9103e5', '안녕하세요')
score = convert_score((float(score)))
print(score)
