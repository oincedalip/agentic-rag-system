from app.graph.workflow import build_graph
from app.graph.state import AgentState


if __name__ == "__main__":
    graph = build_graph()

    initial_state = AgentState(
        query="How should we optimize warehouse operations?"
    )

    result = graph.invoke(initial_state)

    print(result.get("answer"))