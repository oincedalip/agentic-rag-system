from typing import Dict
from app.graph.state import AgentState


class ValidatorAgent:

    def run(self, state: AgentState) -> Dict:

        answer = state.answer

        if answer is None:
            return {"validation_passed": False}

        confidence = 0.9

        return {
            "validation_passed": True,
            "confidence_score": confidence
        }