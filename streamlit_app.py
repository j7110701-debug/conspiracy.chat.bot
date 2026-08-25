import streamlit as st
import google.generativeai as genai
import os
import speech_recognition as sr
from google.cloud import texttospeech
import io

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
    """Convert text to speech using Google Cloud TTS"""
    try:
        client = texttospeech.TextToSpeechClient()
        
        synthesis_input = texttospeech.SynthesisInput(text=text)
        voice = texttospeech.VoiceSelectionParams(
            language_code="en-US",
            ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
        )
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )
        
        response = client.synthesize_speech(
            input=synthesis_input,
            voice=voice,
            audio_config=audio_config
        )
        
        return response.audio_content
    except Exception as e:
        st.error(f"Audio error: {str(e)}")
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
                
                # Generate and play audio if voice was used
                if use_voice:
                    audio_content = text_to_speech(reply)
                    if audio_content:
                        st.audio(audio_content, format="audio/mp3", autoplay=True)
            else:
                placeholder.error("❌ Failed to get a response. Try again.")
                st.session_state.messages.pop()
                
        except Exception as e:
            placeholder.error(f"❌ Error: {str(e)}")
            st.session_state.messages.pop()

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
