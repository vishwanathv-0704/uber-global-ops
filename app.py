import streamlit as st
import json

from src.agents import orchestrator


st.set_page_config(
    page_title="Uber Global Operations Assistant",
    layout="wide"
)

st.title("Uber Global Operations Assistant")
st.write("Agentic AI system for airport operational analysis")


airport_code = st.selectbox(
    "Select Airport",
    ["SFO", "LAX", "JFK"]
)

if st.button("Analyze Airport"):

    with st.spinner("Running agent workflow..."):

        result = orchestrator(airport_code)

    if result.get("status") == "success":

        st.success("Analysis completed successfully")

        operational = result.get(
            "operational_analysis", {}
        )

        resolution = result.get(
            "resolution_analysis", {}
        )

        policy = result.get(
            "policy_checks", {}
        )

        st.subheader("Operational Analysis")
        st.json(operational)

        st.subheader("Recommended Actions")
        st.json(resolution)

        st.subheader("Policy Compliance")
        st.json(policy)

    else:
        st.error(
            result.get(
                "error",
                "Workflow failed"
            )
        )
