import urllib3
import json
import base64
from pydub import AudioSegment

# class pronunciationAssessment:
#     def __init__(self, request)


# m4a 파일 경로
m4a_file_path = "../static/banana.m4a"

# PCM 파일로 저장할 경로와 파일명
pcm_file_path = "C:/ai_metabus/team_project/october/project/nor3st_AI/static/banana_pcm.pcm"

# mp3 파일 불러오기
audio = AudioSegment.from_file(m4a_file_path, format="m4a")

# # 데이터를 16-bit signed PCM 형식으로 변환
# audio = audio.set_sample_width(2)

# # PCM 파일로 저장
# audio.export(pcm_file_path, format="s16le")


# ####
# openApiURL = "http://aiopen.etri.re.kr:8000/WiseASR/PronunciationKor" # 한국어

# accessKey = "17c34f27-babf-4fb7-8353-11dd5f9103e5"  ## 삭제 필요
# # audioFilePath = "C:/ai_metabus/team_project/october/project/nor3st_AI/static/banana.m4a"
# languageCode = "korean"
# script = "바나나"

# # file = open(audioFilePath, "rb")
# file = open(pcm_file_path, "rb")
# audioContents = base64.b64encode(file.read()).decode("utf8")
# file.close()

# requestJson = {   
#     "argument": {
#         "language_code": languageCode,
#         "script": script,
#         "audio": audioContents
#     }
# }

# http = urllib3.PoolManager()
# response = http.request(
#     "POST",
#     openApiURL,
#     headers={"Content-Type": "application/json; charset=UTF-8","Authorization": accessKey},
#     body=json.dumps(requestJson)
# )

# print("[responseCode] " + str(response.status))
# print("[responBody]")
# print(str(response.data,"utf-8"))