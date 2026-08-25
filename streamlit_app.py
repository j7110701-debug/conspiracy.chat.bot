import streamlit as st
import google.generativeai as genai
import os
import pyttsx3
from io import BytesIO

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

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display conversation history
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
                    
                    # Add listen button for response
                    col1, col2 = st.columns([3, 1])
                    with col2:
                        if st.button("🔊 Listen"):
                            try:
                                # Convert text to speech
                                engine = pyttsx3.init()
                                engine.setProperty('rate', 150)  # Speed
                                
                                # Save to bytes
                                audio_buffer = BytesIO()
                                engine.save_to_file(reply, "temp_audio.mp3")
                                engine.runAndWait()
                                
                                # Play audio
                                with open("temp_audio.mp3", "rb") as f:
                                    st.audio(f.read(), format="audio/mp3")
                                
                                # Clean up
                                if os.path.exists("temp_audio.mp3"):
                                    os.remove("temp_audio.mp3")
                            except Exception as e:
                                st.warning(f"Could not generate audio: {str(e)}")
                else:
                    st.error("❌ Failed to get a response from the model. Try again.")
                    # Remove the incomplete user message
                    st.session_state.messages.pop()
                    
            except Exception as e:
                st.error(f"❌ Error communicating with the API: {str(e)}")
                # Remove the incomplete user message
                st.session_state.messages.pop()
