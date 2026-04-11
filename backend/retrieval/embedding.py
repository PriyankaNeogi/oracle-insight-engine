from openai import OpenAI

client = OpenAI()


def get_embedding(text: str):
    """
    Convert text into embedding vector
    """

    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )

    return response.data[0].embedding


def embed_chunks(chunks):
    """
    Convert list of chunks into embeddings
    """

    embeddings = []

    for chunk in chunks:
        emb = get_embedding(chunk)
        embeddings.append({
            "text": chunk,
            "embedding": emb
        })

    return embeddings