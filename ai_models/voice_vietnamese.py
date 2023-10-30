import json
import os
from gtts import gTTS
import urllib3
import urllib.request
import urllib.parse


def make_entire_voice(text):

    global num
    num = 1

    tts = gTTS(text, lang="ko")
    # dir_name = f"lecture_source/voices/{self.filename}"
    dir_name = f"./static/lecture_source/voices/"
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    
    # word_file_name = f"{self.filename}/{self.filename}.mp3"
    # file_path = os.path.join("lecture_source/voices", word_file_name)
    word_file_name = f"{num}.mp3"
    file_path = f'{dir_name}/{word_file_name}' 
    tts.save(file_path)

    num += 1
    
    return file_path



def korean_to_vietnamse(korean):
       
       korean = korean
       client_id = "" 
       client_secret = "" 
    #    encText = urllib3.parse.quote(korean)
       encText = urllib.parse.quote(korean)

       data = "source=ko&target=vi&text=" + encText

       url = "https://openapi.naver.com/v1/papago/n2mt"
       request = urllib.request.Request(url)
       request.add_header("X-Naver-Client-Id",client_id)
       request.add_header("X-Naver-Client-Secret",client_secret)
       response = urllib.request.urlopen(request, data=data.encode("utf-8"))
       rescode = response.getcode()

       if(rescode==200):
           response_body = response.read()
           response_data = json.loads(response_body)
           translated_text = response_data["message"]["result"]["translatedText"]
           return translated_text
       else:
           return f'"Error Code : "{rescode}'
       
