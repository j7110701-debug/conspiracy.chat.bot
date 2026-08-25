import streamlit as st
import google.genai as genai
import os
import requests

# Validate API key
api_key = os.environ.get("GOOGLE_API_KEY")
if not api_key:
    st.error("❌ GOOGLE_API_KEY environment variable not set. Please configure it.")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-3.6-flash")

st.set_page_config(page_title="Conspiracy Chat Bot", page_icon="🤖", layout="wide")
st.title("🤖 Conspiracy Chat Bot")
st.markdown("**Author:** Jimbo")
st.caption("Iterative reasoning on conspiracy theories")
st.markdown("---")
st.markdown("### 🎤 Voice Mode: Press & Hold to Record")

if "messages" not in st.session_state:
    st.session_state.messages = []

def text_to_speech(text):
    """Convert text to speech using free API"""
    try:
        # Using gTTS (Google Text-to-Speech) via API
        url = f"https://tts-api.com/tts?text={text[:200]}&lang=en"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            return response.content
        else:
            return None
    except Exception as e:
        st.warning(f"Could not generate audio: {str(e)}")
        return None

def process_message(prompt, use_voice=False):
    """Process user message and generate response"""
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.write(prompt)
    
    with st.chat_message("assistant"):
        placeholder = st.empty()
        placeholder.write("⏳ Thinking...")
        
        try:
            # Build conversation context for iterative reasoning
            conversation_context = "\n".join(
                [f"{msg['role'].capitalize()}: {msg['content']}" 
                 for msg in st.session_state.messages[:-1]]
            )
            
            response = model.generate_content(
                f"You discuss conspiracy theories in a balanced thought-provoking way.\n\nConversation:\n{conversation_context}\nUser: {prompt}"
            )
            
            if response and response.text:
                reply = response.text
                placeholder.write(reply)  # Replace "Thinking..." with actual response
                st.session_state.messages.append({"role": "assistant", "content": reply})

# Display conversation history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Two input modes

with col1:
    st.markdown("**Text Input:**")
    if prompt := st.chat_input("Or type your question..."):
        process_message(prompt)

