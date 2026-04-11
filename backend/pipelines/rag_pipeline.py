from backend.services.llm_service import generate
from backend.services.sql_service import query_financials
from backend.services.graph_service import query_graph
from backend.services.reranker_service import rerank_chunks


# -------------------------------
# STEP 1: QUERY CLASSIFICATION
# -------------------------------

def classify_query(query: str):
    q = query.lower()

    if any(k in q for k in ["revenue", "profit", "growth", "margin", "cash", "ebitda", "income"]):
        return "sql"

    elif any(k in q for k in ["subsidiary", "ownership", "owns", "relationship", "acquired", "parent"]):
        return "graph"

    elif any(k in q for k in ["risk", "10-k", "10k", "filing", "disclosure", "md&a"]):
        return "rag"

    return "general"


# -------------------------------
# STEP 2: MAIN PIPELINE
# -------------------------------

def rag_pipeline(query: str):
    route = classify_query(query)

    print(f"\n[ROUTE]: {route}")

    # -------------------------------
    # SQL ROUTE
    # -------------------------------
    if route == "sql":
        try:
            result = query_financials(query)

            return {
                "route": "sql",
                "source": "structured_data",
                "answer": result
            }

        except Exception as e:
            print(f"[SQL ERROR] {e}")

    # -------------------------------
    # GRAPH ROUTE
    # -------------------------------
    if route == "graph":
        try:
            result = query_graph(query)

            return {
                "route": "graph",
                "source": "knowledge_graph",
                "answer": result
            }

        except Exception as e:
            print(f"[GRAPH ERROR] {e}")

    # -------------------------------
    # RAG ROUTE (WITH RERANKING)
    # -------------------------------
    if route == "rag":
        try:
            from app.retrieval.qa_chain import ask_question

            raw_result = ask_question(query)

            print("\n[RAG RAW RESULT]:", raw_result)

            # Extract chunks
            if isinstance(raw_result, dict):
                chunks = raw_result.get("main_points", [])
                pages = raw_result.get("source_pages", [])
            else:
                chunks = [str(raw_result)]
                pages = []

            #  RERANKING STEP
            best_chunks = rerank_chunks(query, chunks)

            # Format answer
            answer_text = "\n".join([f"- {c}" for c in best_chunks])

            formatted_answer = f"""
Top Relevant Risk Factors:

{answer_text}

Source Pages: {pages}
"""

            return {
                "route": "rag",
                "mode": "vector_search + rerank",
                "source": "documents",
                "answer": formatted_answer,
                "confidence": "medium"
            }

        except Exception as e:
            print(f"[RAG ERROR] {e}")

    # -------------------------------
    # FALLBACK
    # -------------------------------
    try:
        prompt = f"""
You are an expert financial analyst.

Answer clearly and concisely.

Question:
{query}
"""
        answer = generate(prompt)

        return {
            "route": "fallback",
            "source": "llm_only",
            "answer": answer
        }

    except Exception as e:
        return {
            "route": "error",
            "error": str(e)
        }