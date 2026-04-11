from backend.services.llm_service import generate


def rerank_chunks(query, chunks):
    if len(chunks) <= 3:
        return chunks  # skip reranking if too few

    scored_chunks = []

    for chunk in chunks:
        prompt = f"""
Query: {query}

Text: {chunk}

Score relevance from 1-10. Only number.
"""
        try:
            score = generate(prompt)
            score = int(''.join(filter(str.isdigit, score)) or 0)
        except:
            score = 0

        scored_chunks.append((chunk, score))

    scored_chunks.sort(key=lambda x: x[1], reverse=True)

    return [c[0] for c in scored_chunks[:3]]