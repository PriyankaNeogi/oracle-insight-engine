from langchain_text_splitters import RecursiveCharacterTextSplitter


def chunk_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100
    )

    chunks = splitter.split_documents(documents)

    clean_chunks = []

    for i, chunk in enumerate(chunks):
        text = chunk.page_content.strip()

        # remove useless metadata chunks
        if len(text) < 50:
            continue

        if "pdftex" in text.lower():
            continue

        chunk.metadata["chunk_id"] = i
        clean_chunks.append(chunk)

    return clean_chunks