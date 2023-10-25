import os
import openai
from langchain.document_loaders import DirectoryLoader
from langchain.document_loaders.pdf import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
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
        self.location = request.args["pdf_storage_location"]
        self.embedding = OpenAIEmbeddings()
        self.persist_directory="cromadb"
        #기존에 있던 정보 로드하기
        self.vectordb = Chroma(
            persist_directory=self.persist_directory, 
            embedding_function=self.embedding)
    
    def __enter__(self):
        if self.url == "save_doc":
            self.result["result"] = self.set_up_cromadb()
            return self.result
        elif self.url == "question":
            self.result["answer"] = self.getAnswer()
            return self.result

    def __exit__(self, exc_type, exc_value, traceback):
        pass
    
        
    def getAnswer(self):
        retriever = self.vectordb.as_retriever()  

        llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
        qa_chain = RetrievalQA.from_chain_type(llm, retriever=retriever)
        response = qa_chain({"query": self.question})
        
        return self.chat(response)
    
    def set_up_cromadb(self):
        #새로운 문서가 들어올때 문서 정리해서 cromadb에 저장하기
        loader = DirectoryLoader(self.location, glob="*.pdf", loader_cls=PyPDFLoader, show_progress=True)
        documents = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size = 800, chunk_overlap = 100)
        texts = text_splitter.split_documents(documents)
        # 크로마 db 업데이트하기
        result = Chroma.from_documents(texts, self.embedding, persist_directory=self.embedding)
        return result