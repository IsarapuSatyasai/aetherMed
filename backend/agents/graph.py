from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated, Sequence
import operator
from langchain_core.messages import BaseMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from langchain_core.tools import tool
from backend.config import settings 

# 1. State Definition
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    clinical_flag: bool

# 2. Initialize Hybrid Models
router_llm = ChatOpenAI(
    model="gpt-4o", 
    temperature=0, 
    api_key=settings.OPENAI_API_KEY
)

medgemma_llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0.2,
    api_key=settings.GROQ_API_KEY
)

# 3. Native Tool Wrappers
@tool
def trigger_emergency_tool(reason: str, location: str = "Unknown") -> str:
    """CRITICAL MANDATORY TOOL: Execute immediately if user input contains themes of suicide, self-harm, giving up on life, or severe crisis."""
    from backend.mcp.server import trigger_emergency
    return trigger_emergency(reason, location)

@tool
def get_wellness_routine_tool(emotion: str) -> str:
    """Generates a CBT grounding technique based on emotion."""
    from backend.mcp.server import get_wellness_routine
    return get_wellness_routine(emotion)

@tool
def find_local_clinic_tool(city: str = "Kakinada") -> str:
    """Finds mental health professionals or physical clinics in the specified city."""
    from backend.mcp.server import find_local_clinic
    return find_local_clinic(city)

@tool
def mental_health_rag_tool_wrapper(query: str) -> str:
    """Retrieves counseling knowledge and advice from vector database."""
    from backend.mcp.server import mental_health_rag_tool
    return mental_health_rag_tool(query)

tools = [
    trigger_emergency_tool, 
    get_wellness_routine_tool, 
    find_local_clinic_tool, 
    mental_health_rag_tool_wrapper
]
router_agent = router_llm.bind_tools(tools)

# 4. Nodes
def triage_node(state: AgentState):
    """Determines if the query needs clinical psychological generation or general routing."""
    last_msg = state["messages"][-1].content.lower()
    clinical_keywords = ["diagnosis", "therapy", "trauma", "symptoms", "medication", "feeling", "anxious", "depressed"]
    
    is_clinical = any(word in last_msg for word in clinical_keywords)
    return {"clinical_flag": is_clinical}

def clinical_agent_node(state: AgentState):
    """Uses Groq LPU for sensitive psychological reasoning."""
    sys_prompt = SystemMessage(content="You are a clinical AI. Provide empathetic, medically safe, and scientifically grounded psychological guidance.")
    response = medgemma_llm.invoke([sys_prompt] + state["messages"])
    return {"messages": [response]}

def standard_agent_node(state: AgentState):
    """Uses GPT-4o and MCP Tools for actionable requests (emergencies, exercises, locations)."""
    sys_prompt = SystemMessage(content="You are a support dispatcher. Use tools to help the user. If they are in crisis, use the emergency tool immediately.")
    response = router_agent.invoke([sys_prompt] + state["messages"])
    return {"messages": [response]}

# 5. Conditional Routing
def route_after_triage(state: AgentState):
    if state.get("clinical_flag"):
        return "clinical_agent"
    return "standard_agent"

# Initialize the node that will physically execute your tools
tool_node = ToolNode(tools)

# 6. Build Graph
workflow = StateGraph(AgentState)
workflow.add_node("triage", triage_node)
workflow.add_node("clinical_agent", clinical_agent_node)
workflow.add_node("standard_agent", standard_agent_node)
workflow.add_node("tools", tool_node) # <-- New node added

workflow.set_entry_point("triage")

# Triage decides between Groq (Clinical) and OpenAI (Standard)
workflow.add_conditional_edges("triage", route_after_triage)

# If OpenAI decides to call a tool, route to the tools node. Otherwise, end.
workflow.add_conditional_edges("standard_agent", tools_condition)

# After the tool executes, route BACK to OpenAI so it can formulate the final answer
workflow.add_edge("tools", "standard_agent")

# Groq's clinical agent just talks directly to the user and ends
workflow.add_edge("clinical_agent", END)

safe_space_app = workflow.compile()