from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain.chains import ConversationChain
from langchain.chat_models import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

class MySenior:
    def __init__(self, request) -> None:
        api_key = os.getenv("OPENAI_API_KEY")
        self.role = "you are a helpful senior software engineer"
        self.question = request.args["question"]
        self.chat = ChatOpenAI(openai_api_key=api_key, model="gpt-3.5-turbo")
        
    def getAnswer(self):
        messages = [
            SystemMessage(content=self.role),
            HumanMessage(content= self.question)
        ]
        
        return self.chat(messages)