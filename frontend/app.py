import os
import streamlit as st
import requests
from components import init_session, render_sidebar, render_header

# Streamlit Page Configuration
st.set_page_config(
    page_title="Agentic AI Medical Assistant",
    layout="wide"
)

# Initialize Session State and Sidebar
init_session()
render_sidebar()
render_header()

# FastAPI Endpoint Configuration - Uses Environment Variable!
# Defaults to localhost for local dev, overridden by Docker Compose
API_BASE_URL = os.getenv("API_URL", "http://localhost:8000")
BACKEND_URL = f"{API_BASE_URL}/chat"

# Render Existing Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input Processing
if user_input := st.chat_input("How are you feeling today?"):
    # Append user query to UI state
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Send request to FastAPI backend
    with st.chat_message("assistant"):
        with st.spinner("Orchestrating agent graph and retrieving insights..."):
            try:
                payload = {
                    "session_id": st.session_state.session_id,
                    "message": user_input
                }
                response = requests.post(BACKEND_URL, json=payload, timeout=90)
                
                if response.status_code == 200:
                    bot_response = response.json().get("response", "No response received.")
                    st.markdown(bot_response)
                    st.session_state.messages.append({"role": "assistant", "content": bot_response})
                else:
                    error_msg = f"⚠️ Backend Error ({response.status_code}): Could not complete the agent graph cycle."
                    st.error(error_msg)
            
            except requests.exceptions.ConnectionError:
                # Updated error message dynamically shows the attempted URL
                st.error(f"❌ Connection Failed: Please verify that your FastAPI backend is running at `{API_BASE_URL}`.")
            except Exception as e:
                st.error(f"❌ An unexpected error occurred: {str(e)}")