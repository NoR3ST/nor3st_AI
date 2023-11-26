import os
from dotenv import load_dotenv
from model.Education import Education

from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI

load_dotenv()

class Simulation:
    def __init__(self, request, voice_path) -> None:
        api_key = os.getenv("OPENAI_API_KEY")
        self.chat = ChatOpenAI(openai_api_key=api_key, model_name="gpt-3.5-turbo", temperature=0.1)
        
        self.answer = ""
        with Education(request=request, voice_path=voice_path, url = "text") as result:
            self.answer = result["answer"]
        
        self.model_answer = request.form["model_answer"]
        self.question = request.form["question"]
        template = """질문은 {question}이고 질문에 대한 대답으로 {model_answer}가 정답이야. {user_answer}가 {model_answer}과 답이 유사하고 문법, 어휘가 맞으면 T, 틀리면 F로 한 글자 만으로 말해줘."""
        self.system_message_prompt = SystemMessagePromptTemplate.from_template(template)
        
        self.result = {}
    
    def __enter__(self):
        self.get_answer()
        return self.result

    def __exit__(self, exc_type, exc_value, traceback):
        pass
        
    def get_answer(self):
        if self.answer is None or len(self.answer) < 3:
            return "False"
        
        prompt = ChatPromptTemplate.from_messages([
            self.system_message_prompt
        ])
        
        answer =  self.chat(
            prompt.format_prompt(
                question=self.question, user_answer=self.answer, model_answer = self.model_answer
            ).to_messages()
        )

        if "T" in answer.content:
            self.result["answer"] = True
        else:
            self.result["answer"] = False