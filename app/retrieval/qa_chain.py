from langchain_openai import ChatOpenAI

from app.config.settings import settings
from app.retrieval.retriever import get_retriever


def ask_question(query: str):
    # Step 1: Retrieve relevant documents
    retriever = get_retriever()
    docs = retriever.invoke(query)

    # Step 2: Build context from retrieved docs
    context = "\n\n".join([doc.page_content for doc in docs])

    # Step 3: Initialize LLM
    llm = ChatOpenAI(
        temperature=0,
        openai_api_key=settings.OPENAI_API_KEY
    )

    # Step 4: Improved prompt (structured + clean)
    prompt = f"""
You are an AI research assistant.

Your job:
- Understand the paper deeply
- Ignore metadata, formatting info, or technical headers
- Focus only on meaningful content

Context:
{context}

Question:
{query}

Answer in this format:
1. Main topic
2. Key idea
3. Why it matters (in simple terms)
"""

    # Step 5: Get response
    response = llm.invoke(prompt)
    answer_text = response.content

    # Step 6: Clean and structure output
    points = [
        p.strip()
        for p in answer_text.split("\n")
        if p.strip()
    ]

    # Step 7: Clean source pages (remove duplicates + noise)
    sources = list({
        doc.metadata.get("page")
        for doc in docs
        if doc.metadata.get("page") is not None
    })

    return {
        "main_points": points,
        "source_pages": sources
    }