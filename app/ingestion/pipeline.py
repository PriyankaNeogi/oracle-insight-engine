from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore

from app.config.settings import settings
from app.ingestion.loader import load_documents
from app.ingestion.chunker import chunk_documents
from app.ingestion.embedder import get_embeddings

BATCH_SIZE = 50


def get_pinecone_client():
    return Pinecone(api_key=settings.PINECONE_API_KEY)


def ensure_index(pc, index_name):
    existing_indexes = [i.name for i in pc.list_indexes()]

    if index_name not in existing_indexes:
        pc.create_index(
            name=index_name,
            dimension=1536,
            metric="cosine",
            spec=ServerlessSpec(
                cloud="aws",
                region="us-east-1"
            )
        )


def ingest_file(file_path: str):
    pc = get_pinecone_client()

    index_name = settings.INDEX_NAME
    ensure_index(pc, index_name)

    index = pc.Index(index_name)

    documents = load_documents(file_path)
    chunks = chunk_documents(documents)
    embeddings = get_embeddings()

    vectorstore = PineconeVectorStore.from_documents(
    documents=chunks,
    embedding=embeddings,
    index_name=index_name
    )

    for i in range(0, len(chunks), BATCH_SIZE):
        batch = chunks[i:i + BATCH_SIZE]
        vectorstore.add_documents(batch)
        print(f"Ingested batch {i // BATCH_SIZE + 1}")

    print("Ingestion complete")