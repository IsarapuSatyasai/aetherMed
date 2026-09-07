from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from backend.config import settings

def get_retriever():
    vectorstore = Chroma(
        persist_directory="./chroma_db",
        embedding_function=OpenAIEmbeddings(openai_api_key=settings.OPENAI_API_KEY)
    )
    return vectorstore.as_retriever(search_kwargs={"k": 3})