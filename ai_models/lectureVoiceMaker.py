import json
from gtts import gTTS
import os
import json
import urllib.request

class lectureVoiceMaker:
    def __init__(self, full_text_file_location, filename):
        self.filename = filename
        self.full_text_file_location = full_text_file_location
        self.full_text_list = []
        self.result = []
        with open(self.full_text_file_location, 'r', encoding='utf-8') as jsonFile:
            self.full_text_list = json.load(jsonFile)
            
    def __enter__(self):
        return self.make_json_to_file()
    
    def __exit__(self, exc_type, exc_value, traceback):
        pass
    
    def make_voice(self, text, number):
        tts = gTTS(text, lang="ko")
        dir_name = f"lecture_source/voices/{self.filename}"
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        
        word_file_name = f"{self.filename}/{self.filename}_{number[0]}_{number[1]}.mp3"
        file_path = os.path.join("lecture_source/voices", word_file_name)
        tts.save(file_path)
        return word_file_name
    
    def make_entire_voice(self, text):
        tts = gTTS(text, lang="ko")
        # dir_name = f"lecture_source/voices/{self.filename}"
        dir_name = f"./static/lecture_source/voices/{self.filename}"
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        
        # word_file_name = f"{self.filename}/{self.filename}.mp3"
        # file_path = os.path.join("lecture_source/voices", word_file_name)
        word_file_name = f"{self.filename}.mp3"
        file_path = f'{dir_name}/{word_file_name}' 
        tts.save(file_path)
        
        return file_path
    
    def sentence_to_word(self, full_sentence, number):
        structure_sentence = {
            "full_sentence": {
                "text": full_sentence,
                "voice_file": self.make_voice(full_sentence, [number, 0])
            },
            "words": []
        }
        
        words = full_sentence.split()
        
        for i in range(len(words)):
            word = words[i]
            word_structure = {
                "word": word,
                "voice": self.make_voice(word, [number, i+1])
            }
            structure_sentence["words"].append(word_structure)
        
        return structure_sentence 

    def all_sentence_to_word(self):
        full_text_list = self.full_text_list
        for i in range(len(full_text_list)):
            self.result.append(self.sentence_to_word(full_text_list[i]["korea"], i))
            
            
    def make_json_to_file(self):
        
        self.all_sentence_to_word()
        filepath = os.path.join("lecture_source/file_meta_data", self.filename)
        filename = f"{filepath}.json"
        with open(filename, "w") as file:
            json.dump(self.result, file, indent=4, ensure_ascii=False)


    def korean_to_vietnamse(self, korean):
       
       korean = korean
       client_id = "CLIENT_ID" 
       client_secret = "CLIENT_SECREST" 
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