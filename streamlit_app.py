# This file renamed from 'Streamlit app.py' to 'streamlit_app.py' for consistency
# Original content would go here - importing from main reasoning module

import streamlit as st
import reasoning_iter as reasoning

st.set_page_config(page_title="Conspiracy Chat Bot", layout="wide")

st.title("🤖 Conspiracy Chat Bot")
st.markdown("**Author:** Jimbo")
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
