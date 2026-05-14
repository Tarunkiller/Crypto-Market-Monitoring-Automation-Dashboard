import streamlit as st
import requests
import os

API_URL = os.getenv("API_URL", "http://localhost:8000/api")

def render_chat_ui():
    st.title("🤖 AI Analytics Copilot")
    st.markdown("Ask me anything about the crypto market! I can fetch real-time data, query historical trends, and summarize market reports.")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
        
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            
    # Suggested Prompts
    st.markdown("### Suggested Prompts")
    col1, col2, col3 = st.columns(3)
    if col1.button("Which coin had the highest growth this week?"):
        process_prompt("Which coin had the highest growth this week?")
    if col2.button("Summarize today's market trends."):
        process_prompt("Summarize today's market trends.")
    if col3.button("Show high-risk coins with unusual volatility."):
        process_prompt("Show high-risk coins with unusual volatility.")

    # User Input
    if prompt := st.chat_input("What would you like to know?"):
        process_prompt(prompt)

def process_prompt(prompt: str):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
        
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                res = requests.post(f"{API_URL}/chat", json={"message": prompt})
                res.raise_for_status()
                response = res.json().get("response", "No response.")
            except Exception as e:
                response = f"Sorry, I encountered an error: {e}"
                
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    st.set_page_config(page_title="AI Copilot", layout="wide", page_icon="🤖")
    render_chat_ui()
