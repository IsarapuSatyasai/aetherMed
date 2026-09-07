import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    OPENAI_API_KEY: str = "your_openai_key"
    GROQ_API_KEY: str = "your_groq_key"
    TWILIO_ACCOUNT_SID: str = "your_twilio_sid"
    TWILIO_AUTH_TOKEN: str = "your_twilio_token"
    TWILIO_PHONE_NUMBER: str = "+1234567890"
    EMERGENCY_CONTACT: str = "+0987654321"
    DATABASE_URL: str = "sqlite:///./safespace.db"
    
    LANGCHAIN_TRACING_V2: str = "true"
    LANGCHAIN_API_KEY: str = ""
    LANGCHAIN_PROJECT: str = "Agentic_ai_chatbot"
    OLLAMA_BASE_URL: str = "http://localhost:11434"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()

# Automatically set LangSmith environment variables for the tracer
os.environ["LANGCHAIN_TRACING_V2"] = settings.LANGCHAIN_TRACING_V2
os.environ["LANGCHAIN_API_KEY"] = settings.LANGCHAIN_API_KEY
os.environ["LANGCHAIN_PROJECT"] = settings.LANGCHAIN_PROJECT