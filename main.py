from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List

# Importing your existing logic
from app.graph.workflow import build_graph
from app.graph.state import AgentState

app = FastAPI(title="Agentic Workflow API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Your frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Initialize the graph once at startup
graph = build_graph()

# Request Schema
class QueryRequest(BaseModel):
    query: str
    thread_id: Optional[str] = "default_user"

# Response Schema
class QueryResponse(BaseModel):
    query: str
    answer: str
    plan: List[str]
    confidence: Optional[float] = None

@app.post("/ask", response_model=QueryResponse)
async def ask_agent(request: QueryRequest):
    """
    Triggers the agentic graph and returns the final validated answer.
    """
    try:
        # 1. Initialize State
        initial_state = {
            "query": request.query,
            "plan": [],
            "retrieved_docs": [],
            "answer": None,
            "validation_passed": False
        }

        # 2. Invoke Graph (Standard LangGraph/Custom Graph syntax)
        # Note: Using .invoke() if it's a standard compiled graph
        result = graph.invoke(initial_state)

        # 3. Handle possible failures in the chain
        if not result.get("answer"):
            raise HTTPException(status_code=500, detail="Agent failed to produce an answer.")

        return QueryResponse(
            query=request.query,
            answer=result.get("answer"),
            plan=result.get("plan", []),
            confidence=result.get("confidence_score")
        )

    except Exception as e:
        print(f"API Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    return {"status": "alive", "agents_loaded": True}

