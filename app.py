import os
import streamlit as st
from google import genai
from dotenv import load_dotenv

# Local .env file se variables load karein (local testing ke liye)
load_dotenv()

# Page Config
st.set_page_config(page_title="Brainy Bro", page_icon="🤖")
st.title("🤖 Brainy Bro")

# Streamlit Secrets ya .env se API Key fetch karein
API_KEY = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")

# Client Initialize Karein
client = genai.Client(api_key=API_KEY)

# Chat History Setup
if "messages" not in st.session_state:
    st.session_state.messages = []

# Purane messages screen par dikhane ke liye
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if user_prompt := st.chat_input("Ask to bro....."):
    # Display User Message
    st.chat_message("user").markdown(user_prompt)
    st.session_state.messages.append({"role": "user", "content": user_prompt})

    # Generate Response
    with st.chat_message("assistant"):
        with st.spinner("typing..."):
            try:
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=user_prompt,
                )
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Error aaya: {e}")