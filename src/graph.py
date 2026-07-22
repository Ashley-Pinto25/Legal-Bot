from langgraph.graph import StateGraph, START, END

from src.state import GraphState
from src.classifier import classify_department


def classifier_node(state: GraphState):

    state["department"] = classify_department(
        state["question"]
    )

    return state


workflow = StateGraph(GraphState)

workflow.add_node(
    "classifier",
    classifier_node
)

workflow.add_edge(
    START,
    "classifier"
)

workflow.add_edge(
    "classifier",
    END
)

graph = workflow.compile()