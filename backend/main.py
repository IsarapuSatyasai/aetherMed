from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from backend.database.db_setup import init_db, get_db
from backend.database.models import ChatHistory
from backend.agents.graph import safe_space_app
from langchain_core.messages import HumanMessage

app = FastAPI(title="SafeSpace Agentic API")

class ChatRequest(BaseModel):
    session_id: str
    message: str

@app.on_event("startup")
def on_startup():
    init_db()

@app.post("/chat")
def chat_endpoint(request: ChatRequest, db: Session = Depends(get_db)):
    initial_state = {"messages": [HumanMessage(content=request.message)]}
    config = {"recursion_limit": 10}
    
    try:
        # LangSmith will automatically trace this invocation based on env vars
        result = safe_space_app.invoke(initial_state, config=config)
        final_message = result["messages"][-1].content
    except Exception as e:
        final_message = f"Agent processing failed: {str(e)}"
    
    # Store in PostgreSQL
    chat_log = ChatHistory(
        session_id=request.session_id,
        user_input=request.message,
        agent_response=final_message
    )
    db.add(chat_log)
    db.commit()
    
    return {"response": final_message}