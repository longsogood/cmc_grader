import streamlit as st
import pandas as pd
import time

# Define constants
API_URL = "https://stock.cmcts.ai/c-agent/api/v1/prediction/d8e6fd42-9a4f-4cb5-9820-62356eda3758"

def query(payload):
    # Dummy function for API calls
    return {"response": "dummy"}

def display_record(selected_index):
    # Display the selected record's details
    with st.container():
        st.subheader(f"Question: {st.session_state.updated_df.loc[selected_index, 'Question']}")
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("True answer:")
            st.markdown(st.session_state.updated_df.loc[selected_index, "True answer"])
        with col2:
            st.subheader("Real answer:")
            st.markdown(st.session_state.updated_df.loc[selected_index, "Real answer"])
        st.subheader(f"Score: {st.session_state.updated_df.loc[selected_index, 'Score']}")
        st.subheader(f"Evaluation:")
        st.markdown(st.session_state.updated_df.loc[selected_index, "Note"])

# Streamlit configuration
st.set_page_config(
    layout="wide", 
    initial_sidebar_state="expanded",
)

# Initialize session state variables
if "selected_index" not in st.session_state:
    st.session_state.selected_index = None

if "updated_df" not in st.session_state:
    st.session_state.updated_df = None

if "file_processed" not in st.session_state:
    st.session_state.file_processed = False

# Display the session state for debugging
st.write(st.session_state)

# File uploader logic
uploaded_file = st.file_uploader("Choose a file")
if uploaded_file and not st.session_state.file_processed:
    df = pd.read_csv(uploaded_file)
    st.session_state.updated_df = pd.read_csv("./data/updated-qa-pair.csv")

    # Simulate a progress bar
    progress_text = "Operation in progress. Please wait."
    my_bar = st.progress(0, text=progress_text)
    for percent_complete in range(100):
        time.sleep(0.01)
        my_bar.progress(percent_complete + 1, text=progress_text)
    time.sleep(1)
    my_bar.empty()

    # Mark the file as processed
    st.session_state.file_processed = True

# Display the dataframe if it exists
if st.session_state.updated_df is not None:
    st.dataframe(st.session_state.updated_df)

    # Record selection logic
    selected_index = st.selectbox(
        label="Choose record to show:",
        options=st.session_state.updated_df.index,
        key="record_select"
    )
    display_record(selected_index)