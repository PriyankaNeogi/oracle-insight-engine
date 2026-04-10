import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
    PINECONE_ENV = os.getenv("PINECONE_ENV")
    INDEX_NAME = os.getenv("INDEX_NAME", "rag-index")
    EMBEDDING_MODEL = "text-embedding-3-small"
    SQL_DB_PATH = "data/financials.db"

settings = Settings()