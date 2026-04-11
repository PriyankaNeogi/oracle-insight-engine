def classify_query(query: str):
    q = query.lower()

    if any(k in q for k in ["revenue", "profit", "growth", "margin"]):
        return "sql"

    elif any(k in q for k in ["subsidiary", "ownership"]):
        return "graph"

    elif any(k in q for k in ["risk", "filing", "10-k"]):
        return "rag"

    return "general"