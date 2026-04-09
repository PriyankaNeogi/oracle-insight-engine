from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore

from app.config.settings import settings
from app.ingestion.embedder import get_embeddings


def get_retriever():
    pc = Pinecone(api_key=settings.PINECONE_API_KEY)

    index = pc.Index(settings.INDEX_NAME)

    embeddings = get_embeddings()

    vectorstore = PineconeVectorStore(
    index_name=settings.INDEX_NAME,
    embedding=embeddings
    )

    return vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={
        "k": 8
    }
)
