import os
import streamlit as st
from google import genai

st.set_page_config(page_title="BrainyBro AI", page_icon="🤖")
st.title("BrainyBro AI Chatbot 🤖")

# Safe Key Fetching
API_KEY = None

# Streamlit Secrets se key padhna
try:
    if "GEMINI_API_KEY" in st.secrets:
        API_KEY = st.secrets["GEMINI_API_KEY"]
except Exception:
    pass

# .env file se fallback check
if not API_KEY:
    API_KEY = os.getenv("GEMINI_API_KEY")

# Stop condition
if not API_KEY:
    st.warning("⚠️ API Key nahi mili. Streamlit Secrets ya .env file check karein.")
    st.stop()

# Initialize Client
client = genai.Client(api_key=API_KEY)

# Session state setup for chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display past chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat Input Box (Hamesha render hoga agar code st.stop tak na jaye)
if prompt := st.chat_input("Poochiye kya poochna hai..."):
    # Render user prompt
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response
    with st.chat_message("assistant"):
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt,
            )
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Error: {e}")