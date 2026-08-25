import streamlit as st
import google.generativeai as genai
import os
from google.cloud import speech_v1
from google.cloud import texttospeech_v1
import io

# Validate API keys
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
        # Play audio for assistant messages if available
        if msg["role"] == "assistant" and "audio" in msg:
            st.audio(msg["audio"], format="audio/mp3")

# Create two columns for input methods
col1, col2 = st.columns(2)

with col1:
    # Text input
    if prompt := st.chat_input("Ask about any conspiracy theory..."):
        process_prompt(prompt, use_voice=False)

with col2:
    # Voice input button
    st.markdown("**Or use voice input:**")
    audio_value = st.audio_input("🎤 Click to record your question")
    
    if audio_value is not None:
        try:
            # Convert audio to text using Google Speech-to-Text
            client = speech_v1.SpeechClient()
            
            # Read audio bytes
            audio_bytes = audio_value.read()
            
            # Prepare request
            audio = speech_v1.RecognitionAudio(content=audio_bytes)
            config = speech_v1.RecognitionConfig(
                encoding=speech_v1.RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=16000,
                language_code="en-US",
            )
            
            # Perform transcription
            response = client.recognize(config=config, audio=audio)
            
            if response.results:
                prompt = response.results[0].alternatives[0].transcript
                st.success(f"📝 Heard: {prompt}")
                process_prompt(prompt, use_voice=True)
        except Exception as e:
            st.error(f"❌ Error processing audio: {str(e)}")

def process_prompt(prompt, use_voice=False):
    """Process user prompt and generate response"""
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
                    
                    # Generate audio response if voice was used
                    audio_content = None
                    if use_voice:
                        try:
                            tts_client = texttospeech_v1.TextToSpeechClient()
                            synthesis_input = texttospeech_v1.SynthesisInput(text=reply)
                            voice = texttospeech_v1.VoiceSelectionParams(
                                language_code="en-US",
                                ssml_gender=texttospeech_v1.SsmlVoiceGender.NEUTRAL,
                            )
                            audio_config = texttospeech_v1.AudioConfig(
                                audio_encoding=texttospeech_v1.AudioEncoding.MP3,
                            )
                            
                            tts_response = tts_client.synthesize_speech(
                                input=synthesis_input,
                                voice=voice,
                                audio_config=audio_config,
                            )
                            
                            audio_content = tts_response.audio_content
                            st.audio(audio_content, format="audio/mp3")
                        except Exception as e:
                            st.warning(f"⚠️ Could not generate audio: {str(e)}")
                    
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": reply,
                        "audio": audio_content
                    })
                else:
                    st.error("❌ Failed to get a response from the model. Try again.")
                    st.session_state.messages.pop()
                    
            except Exception as e:
                st.error(f"❌ Error communicating with the API: {str(e)}")
                st.session_state.messages.pop()

# Call function for text input
if prompt := st.chat_input("Ask about any conspiracy theory..."):
    process_prompt(prompt, use_voice=False)
