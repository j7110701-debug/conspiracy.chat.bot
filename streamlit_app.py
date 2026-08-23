import streamlit as st
import google.generativeai as genai
import os

genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

st.set_page_config(page_title="Conspiracy Chat Bot", page_icon="🤖", layout="wide")
st.title("🤖 Conspiracy Chat Bot")
st.markdown("**Author:** Jimbo")
st.caption("Iterative reasoning on conspiracy theories")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if prompt := st.chat_input("Ask about any conspiracy theory..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = model.generate_content(
                f"You discuss conspiracy theories in a balanced thought-provoking way. User asks: {prompt}"
            )
            reply = response.text
            st.write(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})
