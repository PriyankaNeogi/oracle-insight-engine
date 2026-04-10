from backend.pipelines.financial_pipeline import financial_pipeline
from backend.pipelines.rag_pipeline import rag_pipeline


def agent_pipeline(query: str):
    """
    Basic multi-step reasoning
    """

    financial_data = financial_pipeline(query)
    rag_data = rag_pipeline(query)

    return {
        "route": "agent",
        "financial": financial_data,
        "rag": rag_data
    }