import streamlit as st
from init_db import engine
from sqlmodel import Session, select, func
from model import Members, Coaches, Accesscards, Registrations, Courses
from utils import add_member,select_course, add_course, delete_course, delete_member, update_members
import pandas as pd
import datetime
from datetime import datetime
import streamlit as st


def member_list():
    with Session(engine) as session:
        stmt = select(Members)
        results = session.exec(stmt).all()
        data = [row.__dict__ for row in results]
        for entry in data:
            entry.pop('_sa_instance_state', None)
        df = pd.DataFrame(data)
        #df.index = df.index + 1
        return df


# Initialize session state for df if not already set
if "df" not in st.session_state:
    st.session_state.df = member_list()

# Display the current list of coaches in a dataframe
st.write("Current List of Member:")
st.dataframe(st.session_state.df)

st.write("What do you want to do?")

# Create buttons for Add, Modify, and Delete actions
col1, col2, col3 = st.columns(3)
add_button = col1.button("Add Member")
modify_button = col2.button("Modify Member")
delete_button = col3.button("Delete Member")
# # Check if any button is clicked and display the form accordingly
# if add_button or modify_button or delete_button:
#     with form_container:
#         with st.form("add_form"):

if "add_form_member" not in st.session_state:
    st.session_state.add_form_member = False

if "delete_form_member" not in st.session_state:
    st.session_state.delete_form_member = False

if "modify_form_member" not in st.session_state:
    st.session_state.modify_form_member = False

if add_button:
    st.session_state.add_form_member = True
    st.session_state.delete_form_member = False
    st.session_state.modify_form_member = False


if delete_button:
    st.session_state.delete_form_member = True
    st.session_state.add_form_member = False
    st.session_state.modify_form_member = False

if modify_button:
    st.session_state.delete_form_member = False
    st.session_state.add_form_member = False
    st.session_state.modify_form_member = True

if st.session_state.add_form_member:
    with st.container():
        with st.form("add_form"):
            st.write("Enter details for the new member")
            name=st.text_input("Enter your name")
            mail=st.text_input("Enter your mail")
            access=st.text_input("Enter your personnal access number composed of 6 number")
            
            member_add = st.form_submit_button("Submit")

            # Check if the form is submitted and specialty is valid
            if member_add:
                result = add_member(name,mail,access)
                st.success(result)
                st.rerun()

                # Refresh the dataframe after adding a new coach
                st.session_state.df = member_list()
                st.write("Updated List of members:")
                st.session_state.add_form_member = False
                st.dataframe(st.session_state.df)


if st.session_state.delete_form_member:
    with st.container():
        with st.form("add_form"):
            st.write("Enter details to delete a member")
            member_table=member_list()
            members_name=member_table['member_name'].tolist()
            name_to_delete = st.selectbox("Choose a member", members_name)
            member_delete = st.form_submit_button("Submit")
            if member_delete:
                result=delete_member(name_to_delete)
                st.success(result)
                st.rerun()
                st.session_state.df = member_list()
                st.write("Updated List of Members:")
                st.dataframe(st.session_state.df)
                st.session_state.delete_form_member = False

if st.session_state.modify_form_member:
    with st.container():
        with st.form("add_form"):
            st.write("Enter details to modify a member")
            member_table=member_list()
            members_id=member_table['member_id'].tolist()
            id_modify = st.selectbox("Choose a member", members_id)
            name=st.text_input("Enter a new name (Optional)", value="")
            mail=st.text_input("Enter a new mail (Optional)", value="")
            
            modify_member = st.form_submit_button("Submit")
            if modify_member:
                result=update_members(id_modify,name,mail)
                st.success(result)
                st.rerun()
                st.session_state.df = member_list()
                st.write("Updated List of Members:")
                st.dataframe(st.session_state.df)
                st.session_state.modify_form_member = False

#addition of checking of the date before to add a course