from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI

from app.graph.state import AgentState
from app.agents.planner import PlannerAgent
from app.agents.retriever import RetrievalAgent
from app.agents.reasoner import ReasoningAgent
from app.agents.validator import ValidatorAgent

from typing import Literal

llm = ChatOpenAI(model="gpt-4o", temperature=0.0)


planner = PlannerAgent(model_client=llm)
retriever = RetrievalAgent()
reasoner = ReasoningAgent(model_client=llm)
validator = ValidatorAgent(model_client=llm)


def planner_node(state: AgentState):
    return planner.run(state)


def retriever_node(state: AgentState):
    return retriever.run(state)


def reasoner_node(state: AgentState):
    return reasoner.run(state)


def validator_node(state: AgentState):
    return validator.run(state)


def should_retrieve_documents(state: AgentState) -> Literal["retriever", "reasoner"]:
    plan = state.plan

    if "retrieve_documents" in plan:
        return "retriever"
    else:
        return "reasoner"


def build_graph():

    graph = StateGraph(AgentState)

    graph.add_node("planner", planner_node)
    graph.add_node("retriever", retriever_node)
    graph.add_node("reasoner", reasoner_node)
    graph.add_node("validator", validator_node)

    graph.set_entry_point("planner")

    graph.add_conditional_edges("planner", should_retrieve_documents)
    graph.add_edge("retriever", "reasoner")
    graph.add_edge("reasoner", "validator")

    graph.add_edge("validator", END)

    return graph.compile()