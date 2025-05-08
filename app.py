import streamlit as st
import requests
import json

OLLAMA_MODEL = "mistral"
OLLAMA_URL = "http://localhost:11434/api/generate"

st.set_page_config(page_title="Local LLM with Ollama", layout="wide")
st.title("Chat with a local LLM")

# Initialize session state to store chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.text_input("Ask a question")

if st.button("Send") and user_input.strip():
    # Add the new user message to history
    st.session_state.chat_history.append(
        {"role": "user", "content": user_input})

    # Build the full prompt from history
    full_prompt = ""
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            full_prompt += f"User: {message['content']}\n"
        else:
            full_prompt += f"Assistant: {message['content']}\n"
    full_prompt += "Assistant:"

    with st.spinner("Thinking..."):
        response = requests.post(OLLAMA_URL, json={
                                 "model": OLLAMA_MODEL,
                                 "prompt": full_prompt,
                                 "stream": True
                                 },
                                 stream=True
                                 )

        if response.status_code == 200:
            placeholder = st.empty()
            assistant_reply = ""

            for line in response.iter_lines():
                if line:
                    # Each line is a JSON object like: {"response": "partial text"}
                    try:
                        data = line.decode("utf-8")
                        chunk = json.loads(data)
                        partial = chunk.get("response", "")
                        assistant_reply += partial
                        placeholder.markdown(assistant_reply)
                    except Exception as e:
                        st.error(f"Error parsing stream: {e}")
                        break

            # Add assistant response to chat history
            st.session_state.chat_history.append(
                {"role": "assistant", "content": assistant_reply})
        else:
            st.error("Something went wrong. Check the Ollama Server")

# Display chat history below input
st.markdown("---")
for i, message in enumerate(st.session_state.chat_history):
    role = "🧑 You" if message["role"] == "user" else "🤖 Assistant"
    st.markdown(f"**{role}:** {message['content']}")
