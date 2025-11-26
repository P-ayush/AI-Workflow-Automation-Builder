from langgraph.graph import StateGraph,END,START
from app.nodes.extract import extract_entities_node
from app.nodes.normalize import normalize_instruction_node
from app.nodes.generate_dsl import generate_dsl_node
from app.nodes.validate import validate_dsl_node
from app.state import WorkflowState


graph = StateGraph(WorkflowState)

graph.add_node("normalize_instruction_node", normalize_instruction_node)
graph.add_node("extract_entities_node", extract_entities_node)
graph.add_node("generate_dsl_node", generate_dsl_node)
graph.add_node("validate_dsl_node", validate_dsl_node)

graph.add_edge(START, "normalize_instruction_node")
graph.add_edge("normalize_instruction_node", "extract_entities_node")
graph.add_edge("extract_entities_node", "generate_dsl_node")
graph.add_edge("generate_dsl_node", "validate_dsl_node")
graph.add_edge("validate_dsl_node", END)
workflow_graph = graph.compile()
