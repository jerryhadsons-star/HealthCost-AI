"""
HealthCost-AI - Streamlit Web Application
Main user interface for the multi-agent healthcare system
"""
import streamlit as st
import os
from dotenv import load_dotenv

from agents.supervisor import SupervisorAgent

# .env file load (for GOOGLE_API_KEY)
load_dotenv()

st.set_page_config(
    page_title="HealthCost-AI",
    page_icon="🏥",
    layout="wide",
)


# Initialize supervisor in session state
if "supervisor" not in st.session_state:
    try:
        st.session_state.supervisor = SupervisorAgent()
    except Exception as e:
        st.session_state.supervisor = None
        st.error(f"Error initializing SupervisorAgent: {e}")

if "history" not in st.session_state:
    st.session_state.history = []


# Sidebar
with st.sidebar:
    st.title("HealthCost-AI")
    st.markdown(
        """
AI-powered healthcare assistant for:

- 📋 Disease information  
- 🏥 Hospital recommendations  
- 💰 Healthcare cost estimation  

Built for Kaggle 5-Day AI Agents Intensive (Agents for Good).
"""
    )

    if st.button("Clear chat history"):
        st.session_state.history = []
        st.success("History cleared!")


st.title("🏥 HealthCost-AI")
st.subheader("Ask about diseases, hospitals, or healthcare costs")

st.markdown(
    """
Examples you can try:

- *\"What are the symptoms of diabetes?\"*  
- *\"Find best hospitals in Delhi for heart treatment\"*  
- *\"How much does diabetes treatment cost per year?\"*
"""
)

query = st.text_area("Type your question here:", height=100)

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Disease Info"):
        query = "What are the symptoms of diabetes?"
with col2:
    if st.button("Find Hospital"):
        query = "Find hospitals in Delhi for heart treatment"
with col3:
    if st.button("Cost Estimate"):
        query = "How much does diabetes treatment cost per year?"

submit = st.button("Submit", type="primary")

if submit:
    if not query.strip():
        st.warning("Please enter a question first.")
    elif st.session_state.supervisor is None:
        st.error("SupervisorAgent is not initialized. Check your GOOGLE_API_KEY and imports.")
    else:
        with st.spinner("Thinking..."):
            try:
                response_text = st.session_state.supervisor.process(query)
                st.session_state.history.append({"user": query, "bot": response_text})
            except Exception as e:
                response_text = f"Error while processing your question: {e}"

        st.markdown("### Answer")
        st.write(response_text)

if st.session_state.history:
    st.markdown("---")
    st.markdown("### Conversation History")
    for i, item in enumerate(reversed(st.session_state.history), start=1):
        st.markdown(f"**You:** {item['user']}")
        st.markdown(f"**HealthCost-AI:** {item['bot']}")
        st.markdown("---")

st.markdown(
    """
---
*Disclaimer: This app is for informational and educational purposes only.  
It is **not** a substitute for professional medical advice. Please consult a doctor for medical concerns.*
"""
)
