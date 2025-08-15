import streamlit as st

st.header("Course Registration")
st.write("This is the course registration page.")
# Modern Course Registration Page
import streamlit as st
from init_db import engine
from sqlmodel import Session, select
from model import Coaches, Registrations, Courses
from styles import apply_custom_css, create_welcome_card, create_section_header
import pandas as pd


# Apply modern styling
apply_custom_css()

def get_available_courses():
    """Retrieves a list of available courses with coach and registration details.

    This function returns a DataFrame containing all courses, including coach information, participant counts, and availability status. It is used to display courses for registration.

    Returns:
        pd.DataFrame: DataFrame with course details, coach info, participant statistics, and availability.
    """
    with Session(engine) as session:
        # Get all courses first
        courses = session.exec(select(Courses)).all()
        
        data = []
        for course in courses:
            # Get coach details
            coach = session.exec(
                select(Coaches).where(Coaches.coach_id == course.coach_id)
            ).first()
            
            # Count current registrations
            reg_count = len(session.exec(
                select(Registrations)
                .where(Registrations.course_id == str(course.course_id))
            ).all())
            
            if coach:
                data.append({
                    'course_id': course.course_id,
                    'course_name': course.course_name,
                    'time_plan': course.time_plan,
                    'max_capacity': course.max_capacity,
                    'coach_name': coach.coach_name,
                    'coach_specialty': coach.specialty,
                    'current_participants': reg_count,
                    'availability': 'Available' if reg_count < course.max_capacity else 'Full'
                })
        
        return pd.DataFrame(data)

def display_course_browser(courses_df):
    """Displays a browser for available courses with filtering and registration options.

    This function presents available courses in a card format, allowing users to filter, sort, and register for courses. It handles empty and filtered data gracefully and provides interactive registration buttons.

    Args:
        courses_df (pd.DataFrame): DataFrame containing available course data.

    Returns:
        None
    """
    if courses_df.empty:
        st.warning("No courses available at the moment. Please check back later!")
        return

    # Filters
    fcol1, fcol2, fcol3 = st.columns(3)
    with fcol1:
        specialty_filter = st.selectbox("Filter by Specialty", ["All"] + sorted(list(courses_df['coach_specialty'].unique())))
    with fcol2:
        availability_filter = st.selectbox("Availability", ["All", "Available", "Full"])
    with fcol3:
        sort_by = st.selectbox("Sort by", ["Course Date", "Course Name", "Participants"])    

    filtered = courses_df.copy()
    if specialty_filter != "All":
        filtered = filtered[filtered['coach_specialty'] == specialty_filter]
    if availability_filter != "All":
        filtered = filtered[filtered['availability'] == availability_filter]

    if sort_by == "Course Date":
        filtered = filtered.sort_values('time_plan')
    elif sort_by == "Course Name":
        filtered = filtered.sort_values('course_name')
    else:
        filtered = filtered.sort_values('current_participants', ascending=False)

    if filtered.empty:
        st.info("No courses match your current filter criteria.")
        return

    cols = st.columns(2)
    for idx, course in filtered.iterrows():
        with cols[idx % 2]:
            # Date/time formatting
            try:
                dt = pd.to_datetime(course['time_plan'])
                formatted_date = dt.strftime('%B %d, %Y')
                formatted_time = dt.strftime('%H:%M')
            except Exception:
                formatted_date = str(course['time_plan'])
                formatted_time = "Time TBD"

            status_color = "#10B981" if course['availability'] == 'Available' else "#EF4444"
            status_icon = "🟢" if course['availability'] == 'Available' else "⚪"

            # Capacity progress
            total = course['max_capacity'] or 0
            current = course['current_participants']
            pct = (current / total * 100) if total else 0
            if pct < 80:
                bar_color = "#10B981"
            elif pct < 100:
                bar_color = "#F59E0B"
            else:
                bar_color = "#EF4444"

            st.markdown(f"""
            <div style="background: rgba(45,45,45,0.95); padding:1.5rem; border-radius:16px; box-shadow:0 8px 32px rgba(0,0,0,.3); backdrop-filter:blur(10px); border:1px solid rgba(255,255,255,0.1); margin:1rem 0; color:#ffffff;">
                <div style="display:flex; justify-content:space-between; align-items:flex-start; gap:1rem;">
                    <div style="flex:1;">
                        <h3 style="margin:0 0 .45rem 0; font-size:1.4rem; font-weight:600; letter-spacing:.5px;">{course['course_name']}</h3>
                        <p style="color:#cccccc; margin:.25rem 0; font-size:1rem;">Coach: {course['coach_name']}</p>
                        <p style="color:#cccccc; margin:.25rem 0; font-size:1rem;">Specialty: {course['coach_specialty']}</p>
                        <p style="color:#cccccc; margin:.25rem 0; font-size:1rem;">Date: {formatted_date}</p>
                        <p style="color:#cccccc; margin:.25rem 0; font-size:1rem;">Time: {formatted_time}</p>
                        <p style="color:#cccccc; margin:.25rem 0; font-size:1rem;">Capacity: {current}/{total}</p>
                        <div style="margin-top:.6rem; display:flex; gap:.5rem; flex-wrap:wrap; align-items:center;">
                            <span style="background:{status_color}; color:#fff; padding:.25rem .65rem; border-radius:16px; font-size:.7rem; font-weight:500; display:inline-flex; gap:.35rem; align-items:center;">{status_icon} {course['availability']}</span>
                            <span style="background:rgba(75,75,75,0.8); color:#ccc; padding:.25rem .65rem; border-radius:16px; font-size:.7rem;">{current}/{total} registered</span>
                        </div>
                        <div style="margin-top:.7rem;">
                            <div style="background:rgba(255,255,255,0.15); height:8px; border-radius:10px;">
                                <div style="background:{bar_color}; width:{pct}%; height:100%; border-radius:10px;"></div>
                            </div>
                        </div>
                    </div>
                    <div style="font-size:2.2rem; opacity:.22;">🏋️</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Register / full button (no emojis per new style)
            if course['availability'] == 'Available':
                if st.button(f"Register for {course['course_name']}", key=f"reg_{course['course_id']}", use_container_width=True):
                    st.success(f"Successfully registered for {course['course_name']}!")
                    st.balloons()
            else:
                st.button("Course Full", disabled=True, use_container_width=True)

# Page header
st.markdown(create_welcome_card(
    "Browse Available Courses", 
    "Discover and register for exciting fitness classes and training sessions",
    "Member"
), unsafe_allow_html=True)

# Get course data
courses_df = get_available_courses()

# Quick stats
st.markdown(create_section_header("Course Overview", "", "Available fitness classes and programs"), unsafe_allow_html=True)

if not courses_df.empty:
    # Compute stats first
    total_courses = len(courses_df)
    available_courses = len(courses_df[courses_df['availability'] == 'Available'])
    try:
        total_spots = courses_df['max_capacity'].sum() if 'max_capacity' in courses_df.columns else 0
        taken_spots = courses_df['current_participants'].sum() if 'current_participants' in courses_df.columns else 0
        available_spots = max(0, total_spots - taken_spots)
    except Exception:
        available_spots = 0
    specialties = courses_df['coach_specialty'].nunique()

    # Replicate compact white stat card implementation (as in manage_courses.py)
    col1, col2, col3, col4 = st.columns(4)

    card_style = "background:white; padding:1rem 1rem; border-radius:16px; box-shadow:0 2px 6px rgba(0,0,0,0.05); margin:1rem 0; height:110px; display:flex; align-items:center;"
    inner_style = "display:flex; justify-content:space-between; width:100%; align-items:baseline; gap:.5rem;"
    title_style = "color:#0F172A; margin:0; font-size:1.0rem; font-weight:700;"
    value_style = "color:#374151; font-size:1.3rem; font-weight:600;"

    with col1:
        st.markdown(f"""
        <div style=\"{card_style}\">\n  <div style=\"{inner_style}\">\n    <h4 style=\"{title_style}\">Total Courses</h4>\n    <span style=\"{value_style}\">{total_courses}</span>\n  </div>\n</div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div style=\"{card_style}\">\n  <div style=\"{inner_style}\">\n    <h4 style=\"{title_style}\">Available Now</h4>\n    <span style=\"{value_style}\">{available_courses}</span>\n  </div>\n</div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div style=\"{card_style}\">\n  <div style=\"{inner_style}\">\n    <h4 style=\"{title_style}\">Available Spots</h4>\n    <span style=\"{value_style}\">{available_spots}</span>\n  </div>\n</div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div style=\"{card_style}\">\n  <div style=\"{inner_style}\">\n    <h4 style=\"{title_style}\">Specialties</h4>\n    <span style=\"{value_style}\">{specialties}</span>\n  </div>\n</div>
        """, unsafe_allow_html=True)

    # Course browser section
    st.markdown(create_section_header("Available Courses", "", "Browse and register for courses"), unsafe_allow_html=True)
    display_course_browser(courses_df)

else:
    st.warning("📋 No courses are currently available. Please check back later!")
