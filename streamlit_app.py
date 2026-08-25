import streamlit as st
import google.generativeai as genai
import os
import pyttsx3
import speech_recognition as sr
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
st.markdown("---")
st.markdown("### 🎤 Voice Mode: Press & Hold to Record")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display conversation history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Two input modes
col1, col2 = st.columns(2)

with col1:
    st.markdown("**Text Input:**")
    if prompt := st.chat_input("Or type your question..."):
        process_message(prompt)

with col2:
    st.markdown("**Voice Input:**")
    audio_value = st.audio_input("🎤 Click to record")
    
    if audio_value is not None:
        try:
            # Convert audio to text
            recognizer = sr.Recognizer()
            with sr.AudioFile(audio_value) as source:
                audio = recognizer.record(source)
            
            prompt = recognizer.recognize_google(audio)
            st.success(f"📝 You said: {prompt}")
            process_message(prompt, use_voice=True)
        except sr.UnknownValueError:
            st.error("❌ Could not understand audio. Please try again.")
        except sr.RequestError as e:
            st.error(f"❌ Error: {str(e)}")
        except Exception as e:
            st.error(f"❌ Error processing audio: {str(e)}")

def process_message(prompt, use_voice=False):
    """Process user message and generate response"""
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
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
                    st.write(reply)
                    st.session_state.messages.append({"role": "assistant", "content": reply})
                    
                    # Auto-play audio if voice was used
                    if use_voice:
                        try:
                            # Convert text to speech
                            engine = pyttsx3.init()
                            engine.setProperty('rate', 150)  # Speed
                            engine.save_to_file(reply, "response_audio.mp3")
                            engine.runAndWait()
                            
                            # Play audio automatically
                            with open("response_audio.mp3", "rb") as f:
                                st.audio(f.read(), format="audio/mp3", autoplay=True)
                            
                            # Clean up
                            if os.path.exists("response_audio.mp3"):
                                os.remove("response_audio.mp3")
                        except Exception as e:
                            st.warning(f"Could not generate audio: {str(e)}")
                else:
                    st.error("❌ Failed to get a response from the model. Try again.")
                    st.session_state.messages.pop()
                    
            except Exception as e:
                st.error(f"❌ Error communicating with the API: {str(e)}")
                st.session_state.messages.pop()
