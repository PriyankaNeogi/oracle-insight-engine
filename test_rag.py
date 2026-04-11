from backend.pipelines.rag_pipeline import rag_pipeline

while True:
    query = input("\nEnter your query (or 'exit'): ")

    if query.lower() == "exit":
        break

    response = rag_pipeline(query)

    print("\n--- RESPONSE ---")
    print(response)