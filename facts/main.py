from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores.chroma import Chroma
from langchain_community.embeddings import OllamaEmbeddings

embeddings = OllamaEmbeddings(model="deepseek-r1:1.5b")

txt_splitter = CharacterTextSplitter(separator="\n", chunk_size=200, chunk_overlap=0)
loader = TextLoader("facts.txt")
docs = loader.load_and_split(text_splitter=txt_splitter)
db = Chroma.from_documents(docs, embedding=embeddings, persist_directory="emb")

results = db.similarity_search_with_score(
    query="What is an interesting fact about the English language",
    k=4,
)
for result in results:
    print("\n")
    print(result[1])
    print(result[0].page_content)
