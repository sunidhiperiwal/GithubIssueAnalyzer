import streamlit as st
import requests

st.title("GitHub Issue Analyzer")

repo_url = st.text_input("GitHub Repository URL", placeholder="e.g., https://github.com/owner/repo")
issue_number_input = st.text_input("Issue Number", placeholder="Enter any positive no.")

if st.button("Analyze"):
    if not repo_url or not issue_number_input:
        st.warning("Please enter both the repository URL and issue number.")
    else:
        try:
            issue_number = int(issue_number_input)
            with st.spinner("Analyzing issue..."):
                response = requests.post(
                    "http://localhost:8000/analyze",
                    json={"repo_url": repo_url, "issue_number": issue_number}
                )
                if response.ok:
                    result = response.json()
                    st.success("Analysis complete!")
                    st.json(result)
                else:
                    st.error(f"Error: {response.text}")
        except ValueError:
            st.error("Issue number must be a valid integer.")
