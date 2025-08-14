import streamlit as st
import datetime
from utils import registrations, historic_number_registrations, historic_registrations
import streamlit as st
from init_db import engine
from sqlmodel import Session, select, func
import pandas as pd
from model import Courses, Registrations


def courses_list():
    with Session(engine) as session:
        stmt = select(Courses)
        results = session.exec(stmt).all()
        data = [row.__dict__ for row in results]
        for entry in data:
            entry.pop('_sa_instance_state', None)
        df = pd.DataFrame(data)
        #df.index = df.index + 1
        return df
st.title("History")
if "history" not in st.session_state:
    st.session_state.history=False

history_button=st.button('History')
if history_button:
    st.session_state.history=True

if st.session_state.history:
    name=st.text_input('Enter your name')
    see_history=st.button('See history')
    if see_history:
        history=historic_registrations(name)
            #history=pd.DataFrame(history)
        #st.write(f"Registrations history: {history}")
        st.write('historic of registration')
        data = [row.__dict__ for row in history]
        for entry in data:
            entry.pop('_sa_instance_state', None)
        st.dataframe(data)
        history_number=historic_number_registrations(name)
        st.write(f"Number of registrations: {history_number}")

st.title("Registration")
if "df" not in st.session_state:
    st.session_state.df = courses_list()

# Display the current list of coaches in a dataframe
st.write("Current List of Course:")
st.dataframe(st.session_state.df)
if 'stage' not in st.session_state:
    st.session_state.stage = 0
    
progress_text = f"Stage {st.session_state.stage + 1} of 3"
progress_value = (st.session_state.stage + 1) / 3
st.progress(progress_value, text=progress_text)


    
def process_form():
    st.session_state.form_submitted = True

if 'stage' not in st.session_state:
    st.session_state.stage = 0

if st.session_state.stage == 0:
    with st.form("personal_details", enter_to_submit=False):
        st.header("Personal Details")
        name = st.text_input("Name", placeholder="Enter your full name")
        #email = st.text_input("Email", placeholder="Enter your email")
        #password = st.text_input("Password", placeholder="Create password", type="password")
        id_member =st.text_input("Enter your member_id")
        submitted = st.form_submit_button("Next", on_click=process_form)

    if st.session_state.get('form_submitted', False):
        if name and id_member:
            st.session_state.name = name
            st.session_state.id_member = id_member
            st.session_state.stage = 1
            st.session_state.form_submitted = False
            st.rerun()
        else:
            st.error("Please fill in all fields.")
            st.session_state.form_submitted = False

elif st.session_state.stage == 1:
    with st.form("choose_program"):
        st.header("Choose Program")
        courses_table=courses_list()
        courses_id=courses_table['course_id'].tolist()
        course_id = st.selectbox("Choose a course", courses_id)
        submitted = st.form_submit_button("Next", on_click=process_form)

    if st.session_state.get('form_submitted', False):
        if course_id:
            st.session_state.course_id = course_id
            st.session_state.stage = 2
            st.session_state.form_submitted = False
            st.rerun()
        else:
            st.error("Please select a program.")
            st.session_state.form_submitted = False

elif st.session_state.stage == 2:
    st.header("Review submissions")
    st.write(f"member_name: {st.session_state.get('name')}")
    st.write(f"member_id: {st.session_state.get('id_member')}")
    st.write(f"Program: {st.session_state.get('course_id')}")
    
    
    if st.button("Submit"):
        # *** Add details to database ***
        result=registrations(st.session_state.get('id_member'), st.session_state.get('course_id'))
        st.success(result)
        history=historic_registrations(st.session_state.get('name'))
        #history=pd.DataFrame(history)
        #st.write(f"Registrations history: {history}")
        data = [row.__dict__ for row in history]
        for entry in data:
            entry.pop('_sa_instance_state', None)
        st.dataframe(data)
        history_number=historic_number_registrations(st.session_state.get('name'))
        
        st.write(f"Number of registrations: {history_number}")

        #st.session_state.clear()
        st.session_state.stage = 0

if st.session_state.stage > 0 and st.button("Back"):
    st.session_state.stage -= 1

    # Clear data associated with the current stage
    if st.session_state.stage == 0:
        st.session_state.pop('name', None)
        st.session_state.pop('email', None)
        st.session_state.pop('password', None)
    elif st.session_state.stage == 1:
        st.session_state.pop('selected_program', None)
    elif st.session_state.stage == 2:
        st.session_state.pop('selected_date', None)
    elif st.session_state.stage == 3:
        st.session_state.pop('selected_time', None)
    st.rerun()




