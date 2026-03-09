from typing import Dict, List
from app.graph.state import AgentState
from langchain_core.messages import SystemMessage, HumanMessage
from pydantic import BaseModel, Field

class PlannerAgentOutput(BaseModel):
    plan: List[str] = Field(description="List of action item names")

class PlannerAgent:

    def __init__(self, model_client):
        # model_client would be your LLM interface (OpenAI, Gemini, etc.)
        self.model = model_client.with_structured_output(PlannerAgentOutput, include_raw=False)

    def _get_system_prompt(self) -> str:
        return (
            "You are an expert Planning Agent. Your job is to break down a complex user query "
            "into a logical sequence of high-level tasks. \n\n"
            "Available task types: [retrieve_documents, generate_answer, validate_output, web_search, synthesize_report].\n"
            "Respond ONLY with a JSON object containing a key 'plan' which is a list of strings. Each item in the list should be one of the available tasks above."
        )

    def run(self, state: AgentState) -> Dict:
        print("--Planner Agent--")

        user_query = state.query

        response = self.model.invoke([
            SystemMessage(self._get_system_prompt()),
            HumanMessage(f"User Query: {user_query}\n\nBased on this query, create a step-by-step plan.")
            ],
        )

        default_plan = ["retrieve_documents", "generate_answer", "validate_output"]

        try:
            plan = response.plan
        except Exception as e:
            print(f"Error parsing plan: {e}")
            plan = default_plan # Safety default

        return {"plan": plan}
