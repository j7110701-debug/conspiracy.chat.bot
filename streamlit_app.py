# Streamlit UI for Conspiracy Chat Bot - Test Version
# Author: Jimbo

import streamlit as st

st.set_page_config(page_title="Conspiracy Chat Bot", layout="wide")

st.title("🤖 Conspiracy Chat Bot")
st.markdown("**Author:** Jimbo")
st.markdown("---")

st.success("✅ App is running!")

st.write("### Testing imports...")

# Test if reasoning_iter can be imported
try:
    import reasoning_iter
    st.success("✅ reasoning_iter imported successfully")
except Exception as e:
    st.error(f"❌ Error importing reasoning_iter: {e}")

st.write("### API Key Status")
import os
api_key = os.getenv("OPENAI_API_KEY")
if api_key:
    st.success("✅ OPENAI_API_KEY is set")
else:
    st.warning("⚠️ OPENAI_API_KEY is NOT set. Add it to Streamlit Secrets.")

st.write("### Questions")
question = st.text_area("Ask a question:", placeholder="Hello", height=100)

if st.button("Test"):
    st.write(f"Question: {question}")
    st.write(f"API Key present: {bool(api_key)}")
