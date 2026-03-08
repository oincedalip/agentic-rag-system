from langgraph.graph import StateGraph, END

from app.graph.state import AgentState
from app.agents.planner import PlannerAgent
from app.agents.retriever import RetrievalAgent
from app.agents.reasoner import ReasoningAgent
from app.agents.validator import ValidatorAgent


planner = PlannerAgent()
retriever = RetrievalAgent()
reasoner = ReasoningAgent()
validator = ValidatorAgent()


def planner_node(state: AgentState):
    return planner.run(state)


def retriever_node(state: AgentState):
    return retriever.run(state)


def reasoner_node(state: AgentState):
    return reasoner.run(state)


def validator_node(state: AgentState):
    return validator.run(state)


def build_graph():

    graph = StateGraph(AgentState)

    graph.add_node("planner", planner_node)
    graph.add_node("retriever", retriever_node)
    graph.add_node("reasoner", reasoner_node)
    graph.add_node("validator", validator_node)

    graph.set_entry_point("planner")

    graph.add_edge("planner", "retriever")
    graph.add_edge("retriever", "reasoner")
    graph.add_edge("reasoner", "validator")

    graph.add_edge("validator", END)

    return graph.compile()