from backend.services.llm_service import generate
from backend.services.sql_service import run_sql


def generate_sql(query: str) -> str:
    """
    Convert natural language query into SQL.
    """

    prompt = f"""
You are a financial data SQL generator.

Convert the user question into a valid SQL query.

Database schema:
financials(company TEXT, year INT, revenue FLOAT, net_income FLOAT)

Rules:
- Return ONLY SQL
- Do NOT include markdown (no ```sql)
- Do NOT include explanations
- Use correct SQL syntax

Examples:
Q: What is Apple's revenue in 2024?
A: SELECT revenue FROM financials WHERE company = 'Apple' AND year = 2024;

Q: Show net income of Apple in 2024
A: SELECT net_income FROM financials WHERE company = 'Apple' AND year = 2024;

User Question:
{query}
"""

    sql = generate(prompt)
    return sql.strip()


def clean_sql(sql: str) -> str:
    """
    Remove unwanted formatting from LLM-generated SQL.
    """

    cleaned = sql.replace("```sql", "").replace("```", "").strip()

    # Remove accidental prefixes like "sql\n"
    if cleaned.lower().startswith("sql"):
        cleaned = cleaned[3:].strip()

    return cleaned


def financial_pipeline(query: str):
    """
    End-to-end financial query pipeline:
    - Generate SQL
    - Clean SQL
    - Execute SQL
    - Return structured result
    """

    try:
        # Step 1: Generate SQL
        raw_sql = generate_sql(query)

        # Step 2: Clean SQL
        sql_query = clean_sql(raw_sql)

        # Step 3: Execute SQL
        result = run_sql(sql_query)

        return {
            "route": "financial",
            "query": query,
            "sql": sql_query,
            "result": result
        }

    except Exception as e:
        return {
            "route": "financial",
            "error": str(e)
        }