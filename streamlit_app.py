import streamlit as st
import os
from dotenv import load_dotenv
import logging
import reasoning_iter as reasoning

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

st.set_page_config(
    page_title="Conspiracy Chat Bot",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Conspiracy Chat Bot")
st.markdown("**Author:** Jimbo")
st.markdown("Iterative reasoning assistant powered by your choice of AI backend.")

with st.sidebar:
    st.header("⚙️ Configuration")
    backend = st.selectbox(
        "Select Backend:",
        ["openai", "anthropic", "llama"],
        help="Choose which AI backend to use for reasoning"
    )
    show_steps = st.checkbox("Show Internal Steps", value=True)
    st.markdown("---")
    st.markdown("**Backend Status:**")
    if backend == "openai" and os.getenv("OPENAI_API_KEY"):
        st.success("✅ OpenAI configured")
    elif backend == "anthropic" and os.getenv("ANTHROPIC_API_KEY"):
        st.success("✅ Anthropic configured")
    elif backend == "llama" and os.getenv("LLAMA_MODEL_PATH"):
        st.success("✅ Local LLaMA configured")
    else:
        st.warning(f"⚠️ {backend} not configured. Check .env file.")

st.header("Ask a Question")
question = st.text_area(
    "Enter your question:",
    value="Explain Newton's second law.",
    height=150,
    placeholder="Ask anything and I'll reason through it step by step..."
)

col1, col2 = st.columns([1, 5])
with col1:
    submit_button = st.button("🚀 Ask", use_container_width=True)

if submit_button:
    if not question.strip():
        st.error("Please enter a question.")
    else:
        try:
            with st.spinner(f"🤔 Thinking using {backend}... (this may take a few seconds)"):
                result = reasoning.iterative_refine(
                    question,
                    backend=backend,
                    show_steps=show_steps
                )
            
            st.success("✅ Reasoning complete!")
            
            if show_steps:
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.subheader("1️⃣ Initial Answer")
                    st.write(result["initial"])
                
                with col2:
                    st.subheader("2️⃣ Critique")
                    st.write(result["critique"])
                
                with col3:
                    st.subheader("3️⃣ Final Answer")
                    st.write(result["final"])
            else:
                st.subheader("Final Answer")
                st.write(result["final"])
        
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            logger.error(f"Error during reasoning: {e}")

st.markdown("---")
st.markdown(
    """
    ### How it works:
    1. **Initial Answer**: The AI provides an initial response with step-by-step reasoning
    2. **Critique**: The AI critiques its own answer, finding flaws and gaps
    3. **Final Answer**: The AI produces a refined answer addressing the critique
    
    This iterative approach helps catch and correct mistakes!
    """
)
