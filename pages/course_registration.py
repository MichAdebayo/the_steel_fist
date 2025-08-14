import streamlit as st

st.header("Course Registration")
st.write("This is the course registration page.")
# Modern Course Registration Page
import streamlit as st
from init_db import engine
from sqlmodel import Session, select, func
from model import Members, Coaches, Registrations, Courses
from styles import apply_custom_css, create_welcome_card, create_metric_card, create_section_header
import pandas as pd
import plotly.express as px
from datetime import datetime

# Apply modern styling
apply_custom_css()

def get_available_courses():
    """Get all available courses with coach information"""
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
    """Display courses in an attractive card layout"""
    if courses_df.empty:
        st.warning("No courses available at the moment. Please check back later!")
        return
    
    # Filter options
    col1, col2, col3 = st.columns(3)
    with col1:
        specialty_filter = st.selectbox(
            "Filter by Specialty:",
            ["All"] + list(courses_df['coach_specialty'].unique())
        )
    
    with col2:
        availability_filter = st.selectbox(
            "Availability:",
            ["All", "Available", "Full"]
        )
    
    with col3:
        sort_by = st.selectbox(
            "Sort by:",
            ["Course Date", "Course Name", "Participants"]
        )
    
    # Apply filters
    filtered_courses = courses_df.copy()
    if specialty_filter != "All":
        filtered_courses = filtered_courses[filtered_courses['coach_specialty'] == specialty_filter]
    if availability_filter != "All":
        filtered_courses = filtered_courses[filtered_courses['availability'] == availability_filter]
    
    # Apply sorting
    if sort_by == "Course Date":
        filtered_courses = filtered_courses.sort_values('time_plan')
    elif sort_by == "Course Name":
        filtered_courses = filtered_courses.sort_values('course_name')
    elif sort_by == "Participants":
        filtered_courses = filtered_courses.sort_values('current_participants', ascending=False)
    
    # Display courses as cards
    if not filtered_courses.empty:
        cols = st.columns(2)
        for idx, course in filtered_courses.iterrows():
            with cols[idx % 2]:
                availability_color = "#10B981" if course['availability'] == 'Available' else "#EF4444"
                availability_icon = "✅" if course['availability'] == 'Available' else "❌"
                
                # Format date
                try:
                    formatted_date = pd.to_datetime(course['time_plan']).strftime('%B %d, %Y')
                    formatted_time = pd.to_datetime(course['time_plan']).strftime('%H:%M')
                except:
                    formatted_date = str(course['time_plan'])
                    formatted_time = "Time TBD"
                
                st.markdown(f"""
                <div style="background: white; padding: 1.5rem; border-radius: 16px; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1); margin-bottom: 1rem;">
                    <div style="display: flex; justify-content: space-between; align-items: start;">
                        <div style="flex: 1;">
                            <h3 style="margin: 0; color: #ffffff; font-size: 1.3rem;">🎯 {course['course_name']}</h3>
                            <p style="color: #6B7280; margin: 0.5rem 0; font-size: 1rem;">👨‍🏫 Coach: {course['coach_name']}</p>
                            <p style="color: #6B7280; margin: 0.3rem 0;">🏷️ Specialty: {course['coach_specialty']}</p>
                            <p style="color: #6B7280; margin: 0.3rem 0;">📅 {formatted_date}</p>
                            <p style="color: #6B7280; margin: 0.3rem 0;">⏰ {formatted_time}</p>
                            <p style="color: #6B7280; margin: 0.3rem 0;">👥 Max Capacity: {course['max_capacity']}</p>
                            <div style="margin: 1rem 0;">
                                <span style="background: {availability_color}; color: white; padding: 0.3rem 0.8rem; border-radius: 20px; font-size: 0.9rem; font-weight: 500;">
                                    {availability_icon} {course['availability']}
                                </span>
                                <span style="background: #F3F4F6; color: #374151; padding: 0.3rem 0.8rem; border-radius: 20px; font-size: 0.9rem; margin-left: 0.5rem;">
                                    👥 {course['current_participants']}/{course['max_capacity']} registered
                                </span>
                            </div>
                        </div>
                        <div style="font-size: 3rem; opacity: 0.2;">🏋️</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Register button
                if course['availability'] == 'Available':
                    if st.button(f"📝 Register for {course['course_name']}", key=f"register_{course['course_id']}", use_container_width=True):
                        st.success(f"🎉 Successfully registered for {course['course_name']}!")
                        st.balloons()
                else:
                    st.button("❌ Course Full", disabled=True, use_container_width=True)
    else:
        st.info("🔍 No courses match your current filter criteria.")

# Page header
st.markdown(create_welcome_card(
    "Browse Available Courses", 
    "Discover and register for exciting fitness classes and training sessions",
    "Member"
), unsafe_allow_html=True)

# Get course data
courses_df = get_available_courses()

# Quick stats
st.markdown(create_section_header("📊 Course Overview", "🎯", "Available fitness classes and programs"), unsafe_allow_html=True)

if not courses_df.empty:
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_courses = len(courses_df)
        st.markdown("""
        <div style="background: rgba(45, 45, 45, 0.95); padding: 1.5rem; border-radius: 16px; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3); text-align: center; margin: 1rem 0; height: 140px; display: flex; flex-direction: column; justify-content: center;">
            <div style="font-size: 2rem; margin-bottom: 1rem;">🎯</div>
            <h4 style="color: #ffffff; margin: 0; font-size: 1.1rem; line-height: 1.2;">Total Courses</h4>
            <p style="color: #cccccc; margin: 0.5rem 0 0 0; font-size: 0.9rem; font-weight: 500;">{}</p>
        </div>
        """.format(str(total_courses)), unsafe_allow_html=True)
    
    with col2:
        available_courses = len(courses_df[courses_df['availability'] == 'Available'])
        st.markdown("""
        <div style="background: rgba(45, 45, 45, 0.95); padding: 1.5rem; border-radius: 16px; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3); text-align: center; margin: 1rem 0; height: 140px; display: flex; flex-direction: column; justify-content: center;">
            <div style="font-size: 2rem; margin-bottom: 1rem;">✅</div>
            <h4 style="color: #ffffff; margin: 0; font-size: 1.1rem; line-height: 1.2;">Available Now</h4>
            <p style="color: #cccccc; margin: 0.5rem 0 0 0; font-size: 0.9rem; font-weight: 500;">{}</p>
        </div>
        """.format(str(available_courses)), unsafe_allow_html=True)
    
    with col3:
        # Calculate available spots with error handling
        try:
            total_spots = courses_df['max_capacity'].sum() if 'max_capacity' in courses_df.columns else 0
            taken_spots = courses_df['current_participants'].sum() if 'current_participants' in courses_df.columns else 0
            available_spots = max(0, total_spots - taken_spots)  # Ensure non-negative
        except:
            available_spots = 0
        
        st.markdown("""
        <div style="background: rgba(45, 45, 45, 0.95); padding: 1.5rem; border-radius: 16px; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3); text-align: center; margin: 1rem 0; height: 140px; display: flex; flex-direction: column; justify-content: center;">
            <div style="font-size: 2rem; margin-bottom: 1rem;">🪑</div>
            <h4 style="color: #ffffff; margin: 0; font-size: 1.1rem; line-height: 1.2;">Available Spots</h4>
            <p style="color: #cccccc; margin: 0.5rem 0 0 0; font-size: 0.9rem; font-weight: 500;">{}</p>
        </div>
        """.format(str(available_spots)), unsafe_allow_html=True)
    
    with col4:
        specialties = courses_df['coach_specialty'].nunique()
        st.markdown("""
        <div style="background: rgba(45, 45, 45, 0.95); padding: 1.5rem; border-radius: 16px; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3); text-align: center; margin: 1rem 0; height: 140px; display: flex; flex-direction: column; justify-content: center;">
            <div style="font-size: 2rem; margin-bottom: 1rem;">🏷️</div>
            <h4 style="color: #ffffff; margin: 0; font-size: 1.1rem; line-height: 1.2;">Specialties</h4>
            <p style="color: #cccccc; margin: 0.5rem 0 0 0; font-size: 0.9rem; font-weight: 500;">{}</p>
        </div>
        """.format(str(specialties)), unsafe_allow_html=True)
    
    # Course browser
    st.markdown(create_section_header("🎯 Available Courses", "📋", "Browse and register for courses"), unsafe_allow_html=True)
    display_course_browser(courses_df)

else:
    st.warning("📋 No courses are currently available. Please check back later!")
