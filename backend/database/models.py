from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class ChatHistory(Base):
    __tablename__ = "chat_history"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, index=True)
    user_input = Column(Text, nullable=False)
    agent_response = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)