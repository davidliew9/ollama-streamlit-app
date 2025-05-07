import streamlit as st
import requests
import json

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
                                 "stream": True
                                 },
                                 stream=True
                                 )
        if response.status_code == 200:
            placeholder = st.empty()
            full_response = ""

            for line in response.iter_lines():
                if line:
                    data = line.decode("utf-8")
                    # Each line is a JSON object like: {"response": "partial text"}
                    try:
                        # or use `json.loads(data)` if you're cautious
                        chunk = json.loads(data)
                        partial = chunk.get("response", "")
                        full_response += partial
                        placeholder.markdown(full_response)
                    except Exception as e:
                        st.error(f"Error parsing stream: {e}")
                        break
        else:
            st.error("Something went wrong. Check the Ollama Server")
