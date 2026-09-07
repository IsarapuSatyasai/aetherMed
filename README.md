# AetherMed

### Agentic AI-Powered Mental Health Support System

AetherMed is an agentic AI application designed to provide supportive mental-health conversations using **LLMs, LangGraph, RAG, MCP tools, and a FastAPI backend**.

The system can route conversations, retrieve relevant mental-health knowledge, provide wellness techniques, find local clinic information, and trigger an emergency notification workflow.

---

## Architecture

![AetherMed Architecture](images/architecture.png)

---

## Key Features

* Agentic AI workflow using **LangGraph**
* Hybrid LLM architecture using **OpenAI + Groq**
* Mental-health **RAG** with Chroma
* OpenAI embeddings for vector search
* **MCP** based tools
* Emergency notification using **Twilio**
* Wellness and grounding techniques
* Local clinic lookup
* PostgreSQL conversation history
* LangSmith tracing and observability
* Streamlit chat interface
* FastAPI REST API
* Docker Compose support

---

## Tech Stack

| Component             | Technology         |
| --------------------- | ------------------ |
| Frontend              | Streamlit          |
| Backend               | FastAPI            |
| Agent Orchestration   | LangGraph          |
| LLM Framework         | LangChain          |
| LLM                   | OpenAI             |
| LLM                   | Groq               |
| Tool Protocol         | MCP                |
| RAG                   | LangChain + Chroma |
| Embeddings            | OpenAI Embeddings  |
| Database              | PostgreSQL         |
| ORM                   | SQLAlchemy         |
| Emergency Integration | Twilio             |
| Observability         | LangSmith          |
| Containerization      | Docker             |
| Language              | Python 3.11        |

---

## Project Structure

```text
aetherMed/
│
├── backend/
│   ├── agents/
│   │   ├── graph.py
│   │   ├── prompts.py
│   │   └── state.py
│   │
│   ├── database/
│   │   ├── db_setup.py
│   │   └── models.py
│   │
│   ├── evaluations/
│   │   └── guardrails.py
│   │
│   ├── mcp/
│   │   └── server.py
│   │
│   ├── tools/
│   │   ├── emergency_tool.py
│   │   ├── location_tool.py
│   │   └── rag_tool.py
│   │
│   ├── vector_store/
│   │   ├── ingest_data.py
│   │   └── retriever.py
│   │
│   ├── config.py
│   └── main.py
│
├── frontend/
│   ├── app.py
│   └── components.py
│
├── data/
│   └── amod_counseling_dataset.csv
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/IsarapuSatyasai/aetherMed.git
cd aetherMed
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it.

**Windows:**

```bash
.venv\Scripts\activate
```

**Linux/macOS:**

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file:

```env
OPENAI_API_KEY=your_openai_api_key
GROQ_API_KEY=your_groq_api_key

DATABASE_URL=postgresql://aethermed:aethermed123@localhost:5433/aethermed

LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your_langsmith_api_key
LANGCHAIN_PROJECT=AetherMed

TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_PHONE_NUMBER=your_twilio_phone_number
EMERGENCY_CONTACT=your_emergency_contact
```

**Never commit `.env` or API keys to GitHub.**

---

## Run with Docker

Start all services:

```bash
docker compose up --build
```

Services:

```text
Streamlit  → http://localhost:8501
FastAPI    → http://localhost:8000
Swagger    → http://localhost:8000/docs
PostgreSQL → localhost:5433
```

---

## Run Manually

### Start FastAPI

```bash
uvicorn backend.main:app --reload
```

### Start Streamlit

Open another terminal:

```bash
streamlit run frontend/app.py
```

Open:

```text
http://localhost:8501
```

---

## RAG Data Ingestion

AetherMed uses the counseling dataset:

```text
data/amod_counseling_dataset.csv
```

Generate the Chroma vector store:

```bash
python -m backend.vector_store.ingest_data
```

The pipeline is:

```text
CSV
 ↓
Pandas
 ↓
Text Splitting
 ↓
OpenAI Embeddings
 ↓
Chroma Vector Database
```

---

## API

### `POST /chat`

Send a message to the AetherMed agent.

Request:

```json
{
  "session_id": "user-001",
  "message": "I am feeling anxious today."
}
```

Response:

```json
{
  "response": "..."
}
```

---

## Agent Workflow

```text
User Message
     │
     ▼
   Triage
     │
 ┌───┴────┐
 ▼        ▼
Clinical  Standard
Agent     Agent
 │        │
 ▼        ▼
Groq    OpenAI
          │
          ▼
        Tools
          │
    ┌─────┼─────┐
    ▼     ▼     ▼
Emergency RAG  Clinic
    │
    ▼
Final Response
```

---

## Observability

AetherMed supports **LangSmith** tracing.

Configure:

```env
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your_langsmith_api_key
LANGCHAIN_PROJECT=AetherMed
```

This allows you to monitor LLM calls, agent execution, tool calls, and errors.

---

## Safety

AetherMed is a prototype for exploring Agentic AI in mental-health support.

It should not be used for:

* Medical diagnosis
* Emergency decision-making
* Professional psychiatric treatment
* Replacing qualified healthcare professionals

For real-world deployment, additional safety validation, clinical review, authentication, monitoring, and regulatory compliance would be required.

---

## Future Improvements

* Improved crisis detection and safety guardrails
* Persistent LangGraph conversation memory
* RAG evaluation
* Automated testing
* Authentication and authorization
* Production-grade vector database
* API rate limiting
* CI/CD
* Production monitoring

---

## Author

**Author Name**

GitHub: Mention your Github link

Repository: Mention Your Github repo link
