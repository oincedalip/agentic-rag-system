from typing import Dict
from app.graph.state import AgentState
from pydantic import BaseModel, Field
from langchain_core.messages import HumanMessage, SystemMessage


class ValidationAgentOutput(BaseModel):
    validation_passed: bool = Field(description="True if the answer is reliable")
    confidence_score: float = Field(description="Confidence score between 0 and 1 about reliability of the answer")

class ValidatorAgent:
    def __init__(self, model_client):
        self.model = model_client.with_structured_output(ValidationAgentOutput, include_raw=False)

    def _get_system_prompt(self) -> str:
        return (
            "You are a Quality Control Agent. Your task is to evaluate an AI-generated answer."
            "If the answer is I don't know validation is not passed and confidence is zero.\n\n"
            "Criteria:\n"
            "1. FAITHFULNESS: Is the answer supported by the provided context?\n"
            "2. RELEVANCE: Does the answer actually address the user's original query?\n"
            "3. HALLUCINATION: Does it contain facts not found in the context?\n\n"
            "Respond ONLY in JSON format with these keys: \n"
            "{'validation_passed': boolean, 'confidence_score': float (0-1)"
        )

    def run(self, state: AgentState) -> Dict:
        print("--Validator Agent--")

        # Pull all necessary context from state
        query = state.query
        answer = state.answer
        docs = state.retrieved_docs
        
        if not answer:
            return {"validation_passed": False, "confidence_score": 0.0}

        context_text = "\n".join([doc.content for doc in docs])

        # The validation prompt
        validation_request = (
            f"Original Query: {query}\n"
            f"Retrieved Context: {context_text}\n"
            f"Generated Answer: {answer}\n\n"
            "Evaluate the answer based on the context and query."
        )

        print(f"{validation_request = }")

        try:
            response = self.model.invoke([
                SystemMessage(self._get_system_prompt()),
                HumanMessage(validation_request)
                ],
            )   
            
            return response.model_dump()
        except Exception as e:
            print(f"Validation Error: {e}")
            # Fail-safe: if validation fails, assume it's not verified
            return {"validation_passed": False, "confidence_score": 0.0}
      
