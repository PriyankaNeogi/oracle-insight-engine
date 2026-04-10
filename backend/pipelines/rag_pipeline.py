from backend.services.llm_service import generate


def rag_pipeline(query: str):
    """
    RAG pipeline using your existing LangChain + Pinecone setup.
    Falls back to LLM-only response if RAG fails.
    """

    # ---- PRIMARY: EXISTING RAG (PDF-based retrieval) ----
    try:
        from app.retrieval.qa_chain import ask_question

        result = ask_question(query)

        return {
            "route": "rag",
            "mode": "existing_rag",
            "source": "pdf_documents",
            "answer": result
        }

    except Exception as e:
        print(f"[RAG ERROR] Existing RAG failed: {e}")

    # ---- FALLBACK: LLM ONLY ----
    try:
        prompt = f"""
You are a financial and research assistant.

Answer the question clearly and concisely.
If no documents are available, answer based on general knowledge.

Question:
{query}
"""

        answer = generate(prompt)

        return {
            "route": "rag",
            "mode": "fallback_llm",
            "source": "llm_only",
            "answer": answer
        }

    except Exception as e:
        return {
            "route": "rag",
            "mode": "error",
            "error": str(e)
        }