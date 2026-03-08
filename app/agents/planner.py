from typing import Dict
from app.graph.state import AgentState


class PlannerAgent:

    def run(self, state: AgentState) -> Dict:

        query = state.query

        # simple planning logic (can later use LLM)
        plan = [
            "retrieve_documents",
            "generate_answer",
            "validate_output"
        ]

        return {"plan": plan}