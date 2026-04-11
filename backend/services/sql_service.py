import duckdb
import pandas as pd
from backend.services.llm_service import generate

# -------------------------------
# STEP 1: LOAD DATA INTO DATABASE
# -------------------------------

conn = duckdb.connect(database=":memory:")

df = pd.read_csv("data/financials/sample_financials.csv")

conn.execute("CREATE TABLE financials AS SELECT * FROM df")


# -------------------------------
# STEP 2: CLEAN SQL (VERY IMPORTANT)
# -------------------------------

def clean_sql(sql: str):
    """
    Remove ```sql formatting from LLM output
    """
    sql = sql.strip()

    if "```" in sql:
        sql = sql.replace("```sql", "")
        sql = sql.replace("```", "")

    return sql.strip()


# -------------------------------
# STEP 3: GENERATE SQL FROM LLM
# -------------------------------

def generate_sql(query: str):
    prompt = f"""
You are an expert SQL generator.

Table:
financials(company, year, revenue, net_income)

IMPORTANT RULES:
- Apple = AAPL
- Microsoft = MSFT
- Google = GOOG
- Return ONLY SQL
- NO explanation
- NO markdown (no ```)

Example:
Q: What is Apple's revenue in 2024?
A: SELECT revenue FROM financials WHERE company = 'AAPL' AND year = 2024;

Now convert this:

{query}
"""

    return generate(prompt)


# -------------------------------
# STEP 4: EXECUTE SQL
# -------------------------------

def query_financials(query: str):
    try:
        sql = generate_sql(query)

        print("\n[RAW SQL]:", sql)

        cleaned_sql = clean_sql(sql)

        print("[CLEAN SQL]:", cleaned_sql)

        result = conn.execute(cleaned_sql).fetchall()

        return {
            "sql": cleaned_sql,
            "result": result
        }

    except Exception as e:
        return f"SQL query failed: {str(e)}"