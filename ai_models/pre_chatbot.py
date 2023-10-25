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


os.environ["OPENAI_API_KEY"] = ""  # 삭제

# # 만약 추가해서 읽을 pdf 있을 때 사용
# loader = PyPDFLoader("invitation.pdf")
# pages = loader.load_and_split()
# print(len(pages))
# print(pages[0])

# 폴더 안에 있는 모든 pdf 읽기
path = './static/company'
loader = DirectoryLoader(path, glob="*.pdf", loader_cls=PyPDFLoader, show_progress=True)
documents = loader.load()

# text 분리하기
text_splitter = RecursiveCharacterTextSplitter(chunk_size = 800, chunk_overlap = 100)
texts = text_splitter.split_documents(documents)
# print(texts[2:4])
# print(len(texts))

# Chroma DB 생성
persist_directory = 'db'
embedding = OpenAIEmbeddings()

# vectordb = Chroma.from_documents(   # 처음에만 해주면 됨
#     documents=texts, 
#     embedding=embedding,
#     persist_directory=persist_directory)

# # 초기화
# vectordb.persist()
# vectordb = None

vectordb = Chroma(
    persist_directory=persist_directory, 
    embedding_function=embedding)


# 연관 문서 찾기 => search_kwargs={"k": 3} 널으면 답변의 개수 지정 가능
# retriever = vectordb.as_retriever()  
# docs = retriever.get_relevant_documents("What is metabus?")

# for doc in docs:
#     print(doc.metadata["source"])


# QA 챗봇 
retriever = vectordb.as_retriever()  

question = "메타버스아카데미 융합 프로젝트의 목적이 뭐야?"

llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
qa_chain = RetrievalQA.from_chain_type(llm, retriever=retriever)
response = qa_chain({"query": question})
# print(response)