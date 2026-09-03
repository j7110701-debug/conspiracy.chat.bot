# Streamlit UI for Conspiracy Chat Bot
# Author: Jimbo

import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import reasoning module
try:
    import reasoning_iter as reasoning
    HAS_REASONING = True
except Exception as e:
    HAS_REASONING = False
    import_error = str(e)

st.set_page_config(page_title="Conspiracy Chat Bot", layout="wide")

st.title("🤖 Conspiracy Chat Bot")
st.markdown("**Author:** Jimbo")
st.markdown("---")

# Check for API keys
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    st.warning("⚠️ No OPENAI_API_KEY configured!")
    st.info("""
    **To use this app, you need to set up your API keys in Streamlit Cloud:**
    
    1. Go to your app settings on Streamlit Cloud
    2. Click on "Secrets"
    3. Add your API key:
    ```
    OPENAI_API_KEY = "sk-..."
    ```
    
    Alternatively, for other backends:
    - `ANTHROPIC_API_KEY = "sk-ant-..."`
    - `LLAMA_MODEL_PATH = "/path/to/model.gguf"`
    """)
else:
    st.success("✅ API key configured!")

st.markdown("---")

question = st.text_area(
    "Ask a question:",
    placeholder="Explain quantum entanglement",
    height=100
)

backend = st.selectbox(
    "Select AI Backend:",
    ["openai", "anthropic", "llama"],
    index=0
)

show_steps = st.checkbox("Show reasoning steps (initial → critique → final)", value=True)

if st.button("🚀 Ask", use_container_width=True):
    if not question.strip():
        st.error("Please enter a question!")
    elif not api_key:
        st.error("❌ API key not configured. Please set OPENAI_API_KEY in Streamlit secrets.")
    elif not HAS_REASONING:
        st.error(f"❌ Error loading reasoning module: {import_error}")
    else:
        with st.spinner("⏳ Thinking... (this may take 10-30 seconds)"):
            try:
                result = reasoning.iterative_refine(
                    question,
                    backend=backend,
                    show_steps=show_steps
                )
                
                st.success("✅ Reasoning complete!")
                
                if show_steps:
                    st.subheader("1️⃣ Initial Answer")
                    st.write(result.get("initial", ""))
                    
                    st.subheader("2️⃣ Critique")
                    st.write(result.get("critique", ""))
                    
                    st.subheader("3️⃣ Final Answer")
                    st.write(result.get("final", ""))
                else:
                    st.subheader("Final Answer")
                    st.write(result.get("final", ""))
            except Exception as e:
                st.error(f"Error: {e}")
