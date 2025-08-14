# Modern Registration Overview Page
import streamlit as st
from init_db import engine
from sqlmodel import Session, select, func
from model import Members, Coaches, Registrations, Courses
from styles import apply_custom_css, create_welcome_card, create_metric_card, create_section_header
import pandas as pd
import plotly.express as px

# Apply modern styling
apply_custom_css()

def get_registration_data():
    """Get comprehensive registration data with member and course details"""
    with Session(engine) as session:
        # Get all registrations first
        registrations = session.exec(select(Registrations)).all()
        data = []
        for reg in registrations:
            member = session.exec(select(Members).where(Members.member_id == int(reg.member_id))).first()
            course = session.exec(select(Courses).where(Courses.course_id == int(reg.course_id))).first()
            if member and course:
                data.append({
                    'registration_id': reg.registration_id,
                    'member_name': member.member_name,
                    'email': member.email,
                    'course_name': course.course_name,
                    'time_plan': course.time_plan,
                    'registration_date': reg.registration_date
                })
        return pd.DataFrame(data)

# Page header
st.markdown(create_welcome_card(
    "Registration Overview", 
    "View and analyze all course registrations across your gym",
    "Admin"
), unsafe_allow_html=True)

# Get registration data
registrations_df = get_registration_data()

# Quick stats (icons removed)
st.markdown(create_section_header("Registration Statistics", "", "Current registration metrics and insights"), unsafe_allow_html=True)

if not registrations_df.empty:
    col1, col2, col3, col4 = st.columns(4)
    card_style = "background:white; padding:1rem 1rem; border-radius:16px; box-shadow:0 2px 6px rgba(0,0,0,0.05); margin:1rem 0; height:110px; display:flex; align-items:center;"
    inner_style = "display:flex; justify-content:space-between; width:100%; align-items:baseline; gap:.5rem;"
    title_style = "color:#0F172A; margin:0; font-size:1.0rem; font-weight:700;"
    value_style = "color:#374151; font-size:1.3rem; font-weight:600;"

    with col1:
        total_registrations = len(registrations_df)
        st.markdown(f"""
        <div style=\"{card_style}\">\n  <div style=\"{inner_style}\">\n    <h4 style=\"{title_style}\">Total Registrations</h4>\n    <span style=\"{value_style}\">{total_registrations}</span>\n  </div>\n</div>
        """, unsafe_allow_html=True)

    with col2:
        unique_members = registrations_df['member_name'].nunique()
        st.markdown(f"""
        <div style=\"{card_style}\">\n  <div style=\"{inner_style}\">\n    <h4 style=\"{title_style}\">Active Members</h4>\n    <span style=\"{value_style}\">{unique_members}</span>\n  </div>\n</div>
        """, unsafe_allow_html=True)

    with col3:
        unique_courses = registrations_df['course_name'].nunique()
        st.markdown(f"""
        <div style=\"{card_style}\">\n  <div style=\"{inner_style}\">\n    <h4 style=\"{title_style}\">Courses with Registrations</h4>\n    <span style=\"{value_style}\">{unique_courses}</span>\n  </div>\n</div>
        """, unsafe_allow_html=True)

    with col4:
        avg_per_member = total_registrations / unique_members if unique_members > 0 else 0
        st.markdown(f"""
        <div style=\"{card_style}\">\n  <div style=\"{inner_style}\">\n    <h4 style=\"{title_style}\">Avg per Member</h4>\n    <span style=\"{value_style}\">{avg_per_member:.1f}</span>\n  </div>\n</div>
        """, unsafe_allow_html=True)
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Most popular courses
        course_popularity = registrations_df['course_name'].value_counts().head(10)
        if not course_popularity.empty:
            fig1 = px.bar(
                x=course_popularity.values,
                y=course_popularity.index,
                orientation='h',
                title="Most Popular Courses",
                labels={'x': 'Registrations', 'y': 'Course Name'},
                color_discrete_sequence=['#EF233C']
            )
            fig1.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_family="Inter",
                title_font_size=16,
                height=400
            )
            st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        # Registration timeline
        if 'registration_date' in registrations_df.columns:
            registrations_df['registration_date'] = pd.to_datetime(registrations_df['registration_date'])
            daily_registrations = registrations_df.groupby(registrations_df['registration_date'].dt.date).size()
            
            if not daily_registrations.empty:
                fig2 = px.line(
                    x=daily_registrations.index,
                    y=daily_registrations.values,
                    title="Daily Registration Trend",
                    labels={'x': 'Date', 'y': 'Count'},
                    markers=True,
                    color_discrete_sequence=['#EF233C']
                )
                fig2.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_family="Inter",
                    title_font_size=16,
                    height=400
                )
                st.plotly_chart(fig2, use_container_width=True)
    
    # Detailed registrations table
    st.markdown(create_section_header("All Registrations", "", "Complete list of course registrations"), unsafe_allow_html=True)
    
    # Search and filter
    col1, col2 = st.columns(2)
    with col1:
        search_member = st.text_input("🔍 Search by Member Name", placeholder="Enter member name...")
    with col2:
        search_course = st.text_input("🎯 Search by Course Name", placeholder="Enter course name...")
    
    # Apply filters
    filtered_df = registrations_df.copy()
    if search_member:
        filtered_df = filtered_df[filtered_df['member_name'].str.contains(search_member, case=False, na=False)]
    if search_course:
        filtered_df = filtered_df[filtered_df['course_name'].str.contains(search_course, case=False, na=False)]
    
    # Display table with styling
    if not filtered_df.empty:
        st.dataframe(
            filtered_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "registration_id": "Registration ID",
                "member_name": "Member Name",
                "email": "Email",
                "course_name": "Course",
                "time_plan": "Course Date & Time",
                "registration_date": "Registered On"
            }
        )
        
        # Export option
        col1, col2, col3 = st.columns([2, 1, 2])
        with col2:
            st.download_button(
                label="📤 Export to CSV",
                data=filtered_df.to_csv(index=False),
                file_name="registrations.csv",
                mime="text/csv",
                use_container_width=True
            )
    else:
        st.info("🔍 No registrations found matching your search criteria.")

else:
    st.warning("📋 No registration data available. Members need to register for courses first!")
