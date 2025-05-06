import streamlit as st
import requests

OLLAMA_MODEL = "mistral"
OLLAMA_URL = "http://localhost:11434/api/generate"

st.set_page_config(page_title="Local LLM with Ollama", layout="wide")
st.title("Chat with a local LLM")

user_input = st.text_input("Ask a question")

if st.button("Send") and user_input.strip():
    with st.spinner("Thinking..."):
        response = requests.post(OLLAMA_URL, json={
                                 "model": OLLAMA_MODEL,
                                 "prompt": user_input,
                                 "stream": False
        })

        if response.status_code == 200:
            answer = response.json()["response"]
            st.write("Response", answer)
        else:
            st.error("Something went wrong. Check the Ollama Server")

