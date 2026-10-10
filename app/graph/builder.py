from langgraph.graph import END,START,StateGraph
from langgraph.checkpoint.memory import MemorySaver
from app.graph.state import AgentState
from app.graph.nodes import *
def build_graph(checkpointer=None):
    b=StateGraph(AgentState)
    for name,node in [("input_validation",input_validation_node),("planner",planner_node),("tool_selection",tool_selection_node),("approval",approval_node),("research",research_node),("analysis",analysis_node),("verification",verification_node),("guardrail",guardrail_node),("final_response",final_response_node)]: b.add_node(name,node)
    b.add_edge(START,"input_validation")
    b.add_conditional_edges("input_validation",route_after_validation,{"planner":"planner","guardrail":"guardrail"})
    b.add_edge("planner","tool_selection")
    b.add_conditional_edges("tool_selection",route_after_tool_selection,{"approval":"approval","research":"research"})
    b.add_conditional_edges("approval",route_after_approval,{"research":"research","guardrail":"guardrail"}); b.add_edge("research","analysis"); b.add_edge("analysis","verification"); b.add_edge("verification","guardrail"); b.add_edge("guardrail","final_response"); b.add_edge("final_response",END)
    return b.compile(checkpointer=checkpointer or MemorySaver())
