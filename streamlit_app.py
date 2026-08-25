import streamlit as st
import google.generativeai as genai
import os

# Validate API key
api_key = os.environ.get("GOOGLE_API_KEY")
if not api_key:
    st.error("❌ GOOGLE_API_KEY environment variable not set. Please configure it.")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.0-flash")

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
            try:
                # Build conversation context for iterative reasoning
                conversation_context = "\n".join(
                    [f"{msg['role'].capitalize()}: {msg['content']}" 
                     for msg in st.session_state.messages[:-1]]  # Exclude the last user message to avoid duplication
                )
                
                response = model.generate_content(
                    f"You discuss conspiracy theories in a balanced thought-provoking way.\n\nConversation:\n{conversation_context}\nUser: {prompt}"
                )
                
                if response and response.text:
                    reply = response.text
                    st.write(reply)
                    st.session_state.messages.append({"role": "assistant", "content": reply})
                else:
                    st.error("❌ Failed to get a response from the model. Try again.")
                    # Remove the incomplete user message
                    st.session_state.messages.pop()
                    
            except Exception as e:
                st.error(f"❌ Error communicating with the API: {str(e)}")
                # Remove the incomplete user message
                st.session_state.messages.pop()
