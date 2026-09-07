import streamlit as st
import uuid

def init_session():
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())
    if "messages" not in st.session_state:
        st.session_state.messages = []

def render_sidebar():
    with st.sidebar:
        st.title("⚙️ Architecture Inspector")
        st.markdown("---")
        st.code(f"Session:\n{st.session_state.session_id[:8]}...", language="text")
        st.markdown("---")
        st.subheader("🛠️ Active Modules")
        st.markdown("""
        * **Router:** GPT-4o + MCP Tools
        * **Clinical Engine:** Med-Gemma 4b (Local)
        * **Observability:** LangSmith Tracing
        * **Persistence:** PostgreSQL
        """)
        st.markdown("[View Traces in LangSmith](https://smith.langchain.com/)")
        
        if st.button("🗑️ Reset Session"):
            st.session_state.messages = []
            st.session_state.session_id = str(uuid.uuid4())
            st.rerun()

def render_header():
    st.title("🛡️ SafeSpace Enterprise")
    st.caption("Agentic Medical Assistant powered by Med-Gemma & MCP")
    st.markdown("---")