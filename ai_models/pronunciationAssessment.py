import os
import requests
import urllib3
import json
import base64
from pydub import AudioSegment


# 원래 코드
audio_file_path = "./static/hello.m4a"
pcm_file_path = "./static/hello.pcm"

audio = AudioSegment.from_file(audio_file_path, format="m4a")
audio = audio.set_sample_width(2)
audio.export(pcm_file_path, format="s16le")
openApiURL = "http://aiopen.etri.re.kr:8000/WiseASR/PronunciationKor" # 한국어
accessKey = ""  ## 삭제 필요
languageCode = "korean"
script = "안녕하세요"

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

# print("[responseCode] " + str(response.status))
# print("[responBody]")
# print(str(response.data,"utf-8"))

data = json.loads(response.data)
score = data["return_object"]["score"]
print(score)