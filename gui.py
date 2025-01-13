import streamlit as st
import pandas as pd
import requests
API_URL = "https://stock.cmcts.ai/c-agent/api/v1/prediction/d8e6fd42-9a4f-4cb5-9820-62356eda3758"
def query(payload):
    response = requests.post(API_URL, json=payload)
    return response.json()

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

st.set_page_config(
    layout="wide", 
    initial_sidebar_state="expanded",
)

if "selected_index" not in st.session_state:
    st.session_state.selected_index = None

if "updated_df" not in st.session_state:
    st.session_state.updated_df = None

if "file_processed" not in st.session_state:
    st.session_state.file_processed = False

# st.write(st.session_state)
uploaded_file = st.file_uploader("Choose a file")
if uploaded_file and not st.session_state.file_processed:
    df = pd.read_csv(uploaded_file)
    st_df = st.dataframe(df)
    questions = df.loc[df["Real answer"].isna(), "Question"].values
    true_answers = df.loc[df["Real answer"].isna(), "True answer"].values
    condition = df["Real answer"].isna()
    indices = df.index[condition].tolist()

    st.session_state.realAnswer_fill_values = {(index, "Real answer"): "" for index in indices}
    st.session_state.qualityScore_fill_values = {(index, "Score"): "" for index in indices}
    st.session_state.note_fill_values = {(index, "Note"): "" for index in indices}
    
    progress_percent = 0
    progress_bar = st.progress(0.0, text="Processing...")
    
    for index, question, true_answer in zip(indices, questions, true_answers):
        response = query({
            "question": f"""Question: {question}
        True answer: {true_answer}""",
        # "chatId": "https://stock.cmcts.ai/c-agent/api/v1/prediction/84044770-5696-4600-ab12-377985460485"
        # "stream": True
        })
        result = response['agentReasoning'][1]['state']
        st.session_state.realAnswer_fill_values[index, "Real answer"] = result["real_answer"]
        st.session_state.qualityScore_fill_values[index, "Score"] = result["quality_score"]
        st.session_state.note_fill_values[index, "Note"] = result["note"]
        progress_percent += 1/len(indices)
        progress_bar.progress(progress_percent, text="Processing...")
    
    progress_bar.empty()
    st.session_state.file_processed = True

    st.session_state.updated_df = df.copy()
    for (index, col), content in st.session_state.realAnswer_fill_values.items():
        st.session_state.updated_df.loc[index, col] = content
        # print(index, col, '\n', content)

    for (index, col), content in st.session_state.qualityScore_fill_values.items():
        st.session_state.updated_df.loc[index, col] = content
        # print(index, col, '\n', content)

    for (index, col), content in st.session_state.note_fill_values.items():
        st.session_state.updated_df.loc[index, col] = content
        
        
if st.session_state.updated_df is not None:
    st_updated_df = st.dataframe(st.session_state.updated_df)
    selected_index = st.selectbox(label="Choose record to show:",
                                    options=st.session_state.updated_df.index,)
    display_record(selected_index)