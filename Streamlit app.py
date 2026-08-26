import streamlit as
import google.generativeai as genai
import os
import requests 
api_key = os.environ.get("GOOGLE_API_KEY")
if not api_key:
    st.error("GOOGLE_API_KEY not set")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

st.set_page_config(page_title="Conspiracy Chat Bot")
st.title("Conspiracy Chat Bot")
st.markdown("**Author:** Jimbo")
st.caption("Iterative reasoning on conspiracy theories")
st.markdown("---")

if "messages" not in st.session_state:
    st.session_state.messages = []

def process_message(prompt):
    st.session_state.messages.append({"role": "user", "content": prompt})
    response = model.generate_content(prompt)
    st.session_state.messages.append({"role": "assistant", "content": response.text})

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if prompt := st.chat_input("Ask about any conspiracy theory..."):
    process_message(prompt)
    st.rerun()
