from typing import Dict
from app.graph.state import AgentState
from langchain_core.messages import SystemMessage, HumanMessage


class ReasoningAgent:
    def __init__(self, model_client):
        # Your preferred LLM interface
        self.model = model_client

    def _get_system_prompt(self) -> str:
        return (
            "You are a precise Reasoning Agent. Your goal is to answer the user's query "
            "using ONLY the provided context. \n\n"
            "Guidelines:\n"
            "1. If the context doesn't contain the answer, state that you don't know.\n"
            "2. Cite your sources if possible (e.g., [Source 1]).\n"
            "3. Be concise and maintain a professional tone.\n"
            "4. If the user query is a casual conversation, you can give a friendly response"
        )

    def run(self, state: AgentState) -> Dict:
        print("--Reasoning Agent--")

        user_query = state.query
        docs = state.retrieved_docs

        # Format context with identifiers for the LLM to reference
        context_block = "\n".join(
            [f"Source {i+1}: {doc.content}" for i, doc in enumerate(docs)]
        )

        # The synthesis prompt
        user_message = (
            f"Context Information:\n{context_block}\n\n"
            f"User Question: {user_query}\n\n"
            f"Final Answer:"
        )

        # Generate the response
        try:
            response = self.model.invoke([
                SystemMessage(self._get_system_prompt()),
                HumanMessage(user_message)
                ],
            )
            print(response)
            answer = response.content
        except Exception as e:
            print(f"Reasoning Error: {e}")
            answer = "I encountered an error while trying to process the information."

        return {"answer": answer}