from backend.services.llm_service import generate


def classify(query: str) -> str:
    prompt = f"""
    Classify query into one of:
    - financial
    - rag
    - agent

    Query: {query}

    Only return one word.
    """
    return generate(prompt).strip().lower()


def route(query: str):
    route_type = classify(query)

    if "financial" in route_type:
        from backend.pipelines.financial_pipeline import financial_pipeline
        return financial_pipeline(query)

    elif "agent" in route_type:
        from backend.core.agent import agent_pipeline
        return agent_pipeline(query)

    else:
        from backend.pipelines.rag_pipeline import rag_pipeline
        return rag_pipeline(query)