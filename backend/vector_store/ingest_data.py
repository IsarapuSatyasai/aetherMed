import os
import pandas as pd
from langchain_community.document_loaders import DataFrameLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from backend.config import settings

def ingest_amod_data():
    os.environ["OPENAI_API_KEY"] = settings.OPENAI_API_KEY
    csv_path = "data/amod_counseling_dataset.csv"
    
    if not os.path.exists(csv_path):
        print("Dataset not found. Please run the download script first.")
        return
    
    df = pd.read_csv(csv_path).dropna()
    loader = DataFrameLoader(df, page_content_column="Context")
    docs = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    splits = text_splitter.split_documents(docs)

    vectorstore = Chroma.from_documents(
        documents=splits,
        embedding=OpenAIEmbeddings(),
        persist_directory="./chroma_db"
    )
    print("Dataset successfully embedded and stored.")

if __name__ == "__main__":
    ingest_amod_data()