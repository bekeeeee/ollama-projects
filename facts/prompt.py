from langchain.vectorstores.chroma import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain_community.chat_models import ChatOllama

embeddings = OllamaEmbeddings(model="deepseek-r1:1.5b")
db = Chroma(
    persist_directory="emb",
    embedding_function=embeddings,
)
retriever = db.as_retriever()
chat = ChatOllama(model="deepseek-r1:1.5b")

chain = RetrievalQA.from_chain_type(llm=chat, retriever=retriever, chain_type="map_reduce")

result = chain.run("What is an interesting fact about English Language?")

print(result)
