from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from backend.core.router import route

app = FastAPI(title="Oracle Insight Engine")


# -------------------------------
# CORS (important for frontend)
# -------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -------------------------------
# Request schema
# -------------------------------
class QueryRequest(BaseModel):
    query: str


# -------------------------------
# Health check
# -------------------------------
@app.get("/")
def health_check():
    return {
        "status": "running",
        "service": "oracle-insight-engine"
    }


# -------------------------------
# Main query endpoint
# -------------------------------
@app.post("/query")
def query_endpoint(request: QueryRequest):
    try:
        result = route(request.query)

        return JSONResponse(
            content={
                "success": True,
                "data": result
            }
        )

    except Exception as e:
        return JSONResponse(
            content={
                "success": False,
                "error": str(e)
            },
            status_code=500
        )


# -------------------------------
# Simple UI endpoint
# -------------------------------
@app.get("/ui")
def serve_ui():
    return FileResponse("app/frontend/index.html")


# For local testing - python -m uvicorn backend.main:app --reload