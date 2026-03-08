from typing import List, Optional
from pydantic import BaseModel


class RetrievedDocument(BaseModel):
    content: str
    source: str
    score: float


class AgentState(BaseModel):

    # user request
    query: str

    # planner output
    plan: Optional[List[str]] = None

    # RAG results
    retrieved_docs: Optional[List[RetrievedDocument]] = None

    # reasoning output
    answer: Optional[str] = None

    # validation results
    validation_passed: Optional[bool] = None
    confidence_score: Optional[float] = None

    # retries
    retries: int = 0

    # human escalation
    escalate_to_human: bool = False