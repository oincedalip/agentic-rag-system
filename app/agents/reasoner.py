from typing import Dict
from app.graph.state import AgentState


class ReasoningAgent:

    def run(self, state: AgentState) -> Dict:

        docs = state.retrieved_docs

        context = "\n".join([d.content for d in docs])

        answer = f"Based on retrieved documents: {context}"

        return {"answer": answer}