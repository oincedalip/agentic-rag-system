from typing import Dict
from app.graph.state import AgentState, RetrievedDocument


class RetrievalAgent:

    def run(self, state: AgentState) -> Dict:

        query = state.query

        # placeholder retrieval logic
        docs = [
            RetrievedDocument(
                content="Example document",
                source="knowledge_base",
                score=0.92
            )
        ]

        return {"retrieved_docs": docs}