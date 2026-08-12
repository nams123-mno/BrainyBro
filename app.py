import os
import streamlit as st
from dotenv import load_dotenv
from google import genai

# Load .env file
load_dotenv()

st.title("BrainyBro AI Chatbot 🤖")

API_KEY = None

# 1. Check Streamlit Secrets safely (taaki Local/Codespaces par crash na ho)
try:
    API_KEY = st.secrets.get("GEMINI_API_KEY")
except Exception:
    pass

# 2. Agar Secrets mein nahi mila, toh .env se uthao
if not API_KEY:
    API_KEY = os.getenv("GEMINI_API_KEY")

# 3. Agar abhi bhi key nahi mili
if not API_KEY:
    st.error("⚠️ API Key nahi mili! Local chala rahe hain toh .env file check karein, Streamlit Cloud par hain toh Secrets check karein.")
    st.stop()

# Initialize Client
client = genai.Client(api_key=API_KEY)