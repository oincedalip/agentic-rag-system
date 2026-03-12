import streamlit as st
import requests

# --- Page Config ---
st.set_page_config(page_title="AI Warehouse Planner", page_icon="📦", layout="wide")

st.title("📦 Operational KnowHow Agent")
st.markdown("Query the agent about operational procedures")

# --- Sidebar for Status ---
with st.sidebar:
    st.header("System Status")
    try:
        health = requests.get("http://localhost:8000/health").json()
        st.success(f"Backend: {health['status']}")
    except:
        st.error("Backend: Offline")

# --- User Input ---
query = st.text_input("Enter your operational query:", placeholder="e.g., What are the main responsabilities of the Logistics Department")

if st.button("Run Agentic Workflow", type="primary"):
    if not query:
        st.warning("Please enter a query first.")
    else:
        with st.spinner("Agent is thinking (Planning -> Retrieving -> Reasoning -> Validating)..."):
            try:
                # Call the FastAPI backend
                response = requests.post(
                    "http://localhost:8000/ask",
                    json={"query": query}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # --- Display Results in Columns ---
                    col1, col2 = st.columns([1, 2])
                    
                    with col1:
                        st.subheader("📋 Execution Plan")
                        for i, step in enumerate(data['plan']):
                            st.info(f"{i+1}. {step.replace('_', ' ').title()}")
                        
                        if data.get('confidence'):
                            st.metric("Confidence Score", f"{data['confidence'] * 100:.1f}%")

                    with col2:
                        st.subheader("🤖 Agent Response")
                        st.markdown(data['answer'])
                        
                        with st.expander("View Raw JSON Metadata"):
                            st.json(data)
                else:
                    st.error(f"Error: {response.status_code} - {response.text}")
                    
            except Exception as e:
                st.exception(e)

# --- Footer ---
st.divider()
st.caption("Powered by FastAPI + LangGraph Agent Logic")