import streamlit as st
import sys
import os

# allow import from src
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from qa_system import check_eligibility

st.set_page_config(page_title="Course Planner AI", layout="centered")

st.title("🎓 Agentic Course Planner")
st.write("Check course eligibility using AI-powered reasoning")

# input
query = st.text_input("Enter your question (e.g., Can I take CS 225?)")

completed_input = st.text_input(
    "Enter completed courses (comma separated, e.g., CS 125, STAT 200)"
)

if st.button("Check Eligibility"):

    if query and completed_input:
        completed_courses = [c.strip() for c in completed_input.split(",")]

        st.write("### 🧠 Output")

        # capture printed output
        import io
        import contextlib

        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            check_eligibility(query, completed_courses)

        output = buffer.getvalue()

        st.code(output)

    else:
        st.warning("Please enter both query and completed courses.")