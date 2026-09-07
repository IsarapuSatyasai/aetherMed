from langchain_core.tools import tool
from backend.vector_store.retriever import get_retriever

@tool
def mental_health_rag_tool(query: str) -> str:
    """Use this tool when the user asks for mental health advice, expresses anxiety, or needs counseling guidance."""
    retriever = get_retriever()
    docs = retriever.invoke(query)
    return "\n\n".join([doc.page_content + "\nCounselor Response: " + str(doc.metadata.get("Response", "")) for doc in docs])