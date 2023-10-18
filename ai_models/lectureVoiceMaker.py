import json
from gtts import gTTS
import os
import logging

logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class lectureVoiceMaker:
    def __init__(self, full_text_file_location, filename):
        self.filename = filename
        self.full_text_file_location = full_text_file_location
        self.full_text_list = []
        self.result = []
        with open(self.full_text_file_location, 'r') as jsonFile:
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
        logging.debug(self.result)
        with open(filename, "w") as file:
            json.dump(self.result, file, indent=4, ensure_ascii=False)