from langchain.memory import ConversationBufferMemory
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.memory import ConversationSummaryBufferMemory

from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.chains import LLMChain
from langchain.chains import ConversationChain
from langchain.chat_models import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

class MySenior:
    def __init__(self, request) -> None:
        api_key = os.getenv("OPENAI_API_KEY")
        self.myQuestion = request.args["question"]
        
        self.system_template = SystemMessagePromptTemplate.from_template("너는 회사 정보를 기준으로 비한국인인 개발자의 질문인 {question}에 대한 답변을 해주는 한국인 개발자야")
        self.system_message = self.system_template.format(language="KOREAN")
        self.llm = ChatOpenAI(openai_api_key=api_key, model="gpt-3.5-turbo", temperature=0.2, streaming=True, callback=[StreamingStdOutCallbackHandler()])
        self.memory = ConversationSummaryBufferMemory(llm=self.llm, max_token_limit=10, memory_key="chat_history", ai_prefix="한국인 개발자", human_prefix="비한국인 개발자", return_messages=True)

    def getAnswer(self):
        
        prompt = ChatPromptTemplate.from_messages([
            self.system_message,
            MessagesPlaceholder(variable_name="chat_history"),
            HumanMessagePromptTemplate.from_template("{my_question}")
        ])
        
        conversation = LLMChain(
            llm=self.llm,
            prompt=prompt,
            verbose = True,
            memory=self.memory
        )
        
        answer = conversation({"human_input": self.myQuestion})
        
        return answer