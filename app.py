import streamlit as st
import pandas as pd
import random

# --- CONFIGURATION ---
MASTER_EXCEL_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vThZUTmAOchxNCuF9yGhOPadDC1r5i-_TERCUFcM7N2nExIR9C6ZpDdCzgqCnVZhyOI9hzSmH-fmEg_/pub?output=xlsx"

EXAM_TABS = {
    "C_DBADM_2404 (HANA DB)": "DBADM",
    "C_CPI_2506 (Integration Suite)": "CPI",
    "KCNA1": "KCNA1",
    "KCNA2": "KCNA2",
    "KCNA3": "KCNA3",
    "KCNA4": "KCNA4",
    "KCNA5": "KCNA5",
    "KCNA6": "KCNA6"
}

# --- DATA LOADING ---
@st.cache_data(ttl=60)
def get_quiz_data(url, sheet_name):
    try:
        df = pd.read_excel(url, sheet_name=sheet_name, engine='openpyxl')
        df.columns = df.columns.str.strip()
        quiz_data = []
        for index, row in df.iterrows():
            opts = []
            for col in df.columns:
                if col.startswith('Option'):
                    val = str(row[col])
                    if val.lower() != 'nan' and val.strip() != '' and val.lower() != 'none':
                        opts.append(val)
            if 'Question' in row and 'Answer' in row:
                quiz_data.append({
                    "question": str(row['Question']),
                    "options": opts, 
                    "answer": str(row['Answer']).strip()
                })
        return quiz_data
    except Exception as e:
        st.error(f"⚠️ Error loading data: {e}")
        return []

# --- APP LOGIC ---
st.set_page_config(page_title="SAP Exam Prep", page_icon="🎓")
st.title("Exam Prep Master 🎓")

# Sidebar
selected_exam_label = st.sidebar.selectbox("Select Exam:", list(EXAM_TABS.keys()))
selected_tab_name = EXAM_TABS[selected_exam_label]

# Initialize State
if 'current_exam' not in st.session_state or st.session_state.current_exam != selected_exam_label:
    st.session_state.current_exam = selected_exam_label
    st.session_state.raw_data = get_quiz_data(MASTER_EXCEL_URL, selected_tab_name)
    st.session_state.current_index = 0
    st.session_state.score = 0
    st.session_state.finished = False
    st.session_state.answer_submitted = False  # NEW: Track if user clicked submit
    st.session_state.feedback = None           # NEW: Store feedback text/color
    
    if st.session_state.raw_data:
        st.session_state.quiz_data = st.session_state.raw_data.copy()
        random.shuffle(st.session_state.quiz_data)
        for q in st.session_state.quiz_data:
            random.shuffle(q["options"])
    else:
        st.session_state.quiz_data = []

if not st.session_state.quiz_data:
    st.warning("No data found!")
    st.stop()

# --- FUNCTIONS ---
def submit_answer():
    q = st.session_state.quiz_data[st.session_state.current_index]
    ans_str = str(q["answer"])
    correct_answers = [x.strip() for x in ans_str.split(';')]
    
    user_selected = []
    for opt in q["options"]:
        key = f"q{st.session_state.current_index}_{opt}"
        if st.session_state.get(key, False):
            user_selected.append(opt)
    
    # Check logic
    if set(user_selected) == set(correct_answers):
        st.session_state.score += 1
        st.session_state.feedback = "correct"
    else:
        st.session_state.feedback = "wrong"
    
    st.session_state.answer_submitted = True # Lock the state to show feedback

def next_question():
    st.session_state.answer_submitted = False # Reset for next question
    st.session_state.feedback = None
    
    if st.session_state.current_index + 1 < len(st.session_state.quiz_data):
        st.session_state.current_index += 1
    else:
        st.session_state.finished = True

def restart_quiz():
    st.session_state.current_index = 0
    st.session_state.score = 0
    st.session_state.finished = False
    st.session_state.answer_submitted = False
    random.shuffle(st.session_state.quiz_data)
    for q in st.session_state.quiz_data:
        random.shuffle(q["options"])

# --- UI RENDERING ---
if st.session_state.finished:
    st.balloons()
    score = st.session_state.score
    total = len(st.session_state.quiz_data)
    st.success(f"Exam Completed! 🏆\n\nYour Score: **{score} / {total}** ({round(score/total*100)}%)")
    st.button("Retake Exam", on_click=restart_quiz, type="primary")

else:
    q = st.session_state.quiz_data[st.session_state.current_index]
    
    # 1. Question Area
    st.progress((st.session_state.current_index) / len(st.session_state.quiz_data))
    st.caption(f"Question {st.session_state.current_index + 1} of {len(st.session_state.quiz_data)}")
    st.markdown(f"### {q['question']}")
    
    if ";" in str(q["answer"]):
        st.info("ℹ️ Select all that apply")
    
    # 2. Options (Disable them if answer is already submitted)
    for opt in q["options"]:
        st.checkbox(opt, key=f"q{st.session_state.current_index}_{opt}", disabled=st.session_state.answer_submitted)

    st.write("---")

    # 3. Action Buttons & Feedback
    if st.session_state.answer_submitted:
        # SHOW FEEDBACK
        if st.session_state.feedback == "correct":
            st.success("✅ Correct!")
        else:
            st.error(f"❌ Wrong! \n\n**Correct Answer:** \n{q['answer'].replace(';', ', ')}")
        
        # NEXT BUTTON
        st.button("Next Question ➡️", on_click=next_question, type="primary")
        
    else:
        # SUBMIT BUTTON
        st.button("Submit Answer", on_click=submit_answer, type="primary")
