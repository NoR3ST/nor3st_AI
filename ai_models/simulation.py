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
    def __init__(self, request) -> None:
        api_key = os.getenv("OPENAI_API_KEY")
        self.chat = ChatOpenAI(openai_api_key=api_key, model_name="gpt-3.5-turbo", temperature=0.1)
        
        self.answer = ""
        with Education(request=request, url = "text") as result:
            self.answer = result["answer"]["segments"][0]["text"]

        self.question = request.form["question"]
        template = """질문은 {question}이고 질문에 대한 대답으로 {answer}가 맥락, 어휘, 문법에 맞다면 TRUE, 문법에 틀리면 FALSE 만으로 리턴해줘."""
        self.system_message_prompt = SystemMessagePromptTemplate.from_template(template)
        
        self.result = {}
    
    def __enter__(self):
        
        return self.get_answer()

    def __exit__(self, exc_type, exc_value, traceback):
        pass
        
    def get_answer(self):
        if len(self.answer) < 3:
            return "False"
        
        prompt = ChatPromptTemplate.from_messages([
            self.system_message_prompt
        ])
        
        answer =  self.chat(
            prompt.format_prompt(
                question=self.question, answer=self.answer
            ).to_messages()
        )
        return answer.content