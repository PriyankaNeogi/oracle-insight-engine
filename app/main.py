from fastapi import FastAPI

from app.ingestion.pipeline import ingest_file
from app.retrieval.qa_chain import ask_question

app = FastAPI()


@app.get("/")
def health_check():
    return {"status": "running"}


@app.post("/ingest")
def ingest():
    file_path = "data/Research_paper.pdf"
    ingest_file(file_path)
    return {"message": "File ingested successfully"}


@app.get("/ask")
def ask(q: str):
    return ask_question(q)


# To run the app, 
# export PYTHONPATH=. uvicorn 
## app.main:app --reload
# open http://127.0.0.1:8000/docs in your browser to access the endpoints