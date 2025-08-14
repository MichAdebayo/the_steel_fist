import streamlit as st
import datetime
from utils import registrations, historic_number_registrations, historic_registrations
from init_db import engine
from sqlmodel import Session, select, func
import pandas as pd
from model import Courses, Registrations
from styles import apply_custom_css, create_welcome_card, create_metric_card, create_section_header
import plotly.express as px
import plotly.graph_objects as go

# Apply styling
apply_custom_css()

def courses_list():
    """Get list of available courses with enhanced information"""
    with Session(engine) as session:
        stmt = select(Courses)
        results = session.exec(stmt).all()
        data = []
        for row in results:
            # Count current registrations
            reg_count = len(session.exec(
                select(Registrations)
                .where(Registrations.course_id == str(row.course_id))
            ).all())
            
            data.append({
                'course_id': row.course_id,
                'course_name': row.course_name,
                'time_plan': row.time_plan,
                'max_capacity': row.max_capacity,
                'coach_id': row.coach_id,
                'current_registrations': reg_count,
                'availability': 'Available' if reg_count < row.max_capacity else 'Full'
            })
        
        df = pd.DataFrame(data)
        return df

def display_course_cards(courses_df):
    """Display courses as modern cards"""
    if courses_df.empty:
        st.warning("No courses available at the moment.")
        return
    
    cols = st.columns(2)
    for idx, course in courses_df.iterrows():
        with cols[idx % 2]:
            availability_color = "🟢" if course['availability'] == 'Available' else "🔴"
            capacity_percentage = (course['current_registrations'] / course['max_capacity']) * 100
            
            st.markdown(f"""
            <div class="course-card">
                <div style="display: flex; justify-content: between; align-items: start; margin-bottom: 1rem;">
                    <div>
                        <h3 style="margin: 0; color: #1F2937; font-size: 1.3rem;">{availability_color} {course['course_name']}</h3>
                        <p style="color: #6B7280; margin: 0.5rem 0;">Coach ID: {course['coach_id']}</p>
                        <p style="color: #6B7280; margin: 0; font-size: 0.9rem;">📅 {course['time_plan'].strftime('%Y-%m-%d %H:%M')}</p>
                    </div>
                </div>
                <div style="background: #F3F4F6; padding: 0.75rem; border-radius: 8px; margin-top: 1rem;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-size: 0.9rem; color: #6B7280;">Capacity:</span>
                        <span style="font-weight: 600; color: #1F2937;">{course['current_registrations']}/{course['max_capacity']}</span>
                    </div>
                    <div style="background: #E5E7EB; border-radius: 10px; height: 8px; margin-top: 0.5rem;">
                        <div style="background: {'#10B981' if capacity_percentage < 80 else '#F59E0B' if capacity_percentage < 100 else '#EF4444'}; 
                                    width: {capacity_percentage}%; height: 100%; border-radius: 10px;"></div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

def create_registration_history_chart(registrations_data):
    """Create a chart showing registration history"""
    if not registrations_data:
        return None
    
    # Convert to dataframe for plotting
    df = pd.DataFrame([{
        'registration_date': reg.registration_date,
        'course_id': reg.course_id
    } for reg in registrations_data])
    
    if df.empty:
        return None
    
    # Group by month for trend
    df['month'] = pd.to_datetime(df['registration_date']).dt.to_period('M')
    monthly_count = df.groupby('month').size().reset_index(name='count')
    monthly_count['month'] = monthly_count['month'].astype(str)
    
    fig = px.line(monthly_count, x='month', y='count', 
                  title='Your Registration Activity',
                  labels={'month': 'Month', 'count': 'Registrations'})
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_family="Inter",
        title_font_size=16,
        height=300
    )
    fig.update_traces(line_color='#4F46E5', line_width=3)
    
    return fig

# Main page header
st.markdown(create_welcome_card(
    "Course Registration", 
    "Register for your favorite fitness classes and track your progress",
    "Member"
), unsafe_allow_html=True)

# Tabs for different sections
tab1, tab2 = st.tabs(["🎯 Register for Courses", "📊 My Activity"])

with tab1:
    st.markdown(create_section_header("Available Courses", "🏃‍♂️", "Browse and register for available fitness classes"), unsafe_allow_html=True)
    
    # Load courses
    if "df" not in st.session_state:
        st.session_state.df = courses_list()
    
    # Course filter
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("🔄 Refresh Courses", use_container_width=True):
            st.session_state.df = courses_list()
            st.rerun()
    
    # Display courses as cards
    display_course_cards(st.session_state.df)
    
    st.markdown("---")
    
    # Registration form
    st.markdown(create_section_header("Quick Registration", "📝", "Register for a course in 3 simple steps"), unsafe_allow_html=True)
    
    # Progress tracking
    if 'stage' not in st.session_state:
        st.session_state.stage = 0
    
    progress_text = f"Step {st.session_state.stage + 1} of 3"
    progress_value = (st.session_state.stage + 1) / 3
    st.progress(progress_value, text=progress_text)
    
    def process_form():
        st.session_state.form_submitted = True
    
    if st.session_state.stage == 0:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        with st.form("personal_details", clear_on_submit=False):
            st.markdown("#### 👤 Personal Information")
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("Full Name", placeholder="Enter your full name", help="Your registered name in the system")
            with col2:
                id_member = st.text_input("Member ID", placeholder="Enter your member ID", help="Your unique member identification number")
            
            submitted = st.form_submit_button("➡️ Continue", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        if submitted:
            if name and id_member:
                st.session_state.name = name
                st.session_state.id_member = id_member
                st.session_state.stage = 1
                st.success("✅ Personal information saved!")
                st.rerun()
            else:
                st.error("❌ Please fill in all required fields.")

    elif st.session_state.stage == 1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        with st.form("choose_program"):
            st.markdown("#### 🎯 Choose Your Course")
            courses_table = courses_list()
            
            if not courses_table.empty:
                # Display course options in a more visual way
                course_options = {}
                for _, course in courses_table.iterrows():
                    status = "✅ Available" if course['availability'] == 'Available' else "❌ Full"
                    course_display = f"{course['course_name']} - {course['time_plan'].strftime('%Y-%m-%d %H:%M')} ({status})"
                    course_options[course_display] = course['course_id']
                
                selected_course_display = st.selectbox(
                    "Select a course:",
                    list(course_options.keys()),
                    help="Choose from available courses. Full courses cannot be selected."
                )
                course_id = course_options[selected_course_display]
            else:
                st.warning("No courses available.")
                course_id = None
            
            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button("⬅️ Back"):
                    st.session_state.stage = 0
                    st.rerun()
            with col2:
                submitted = st.form_submit_button("➡️ Continue", type="primary")
        st.markdown('</div>', unsafe_allow_html=True)

        if submitted and course_id:
            st.session_state.course_id = course_id
            st.session_state.stage = 2
            st.success("✅ Course selected!")
            st.rerun()

    elif st.session_state.stage == 2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown("#### 📋 Review Your Registration")
        
        # Display summary
        st.markdown(f"""
        <div style="background: #F8FAFC; padding: 1.5rem; border-radius: 12px; border-left: 4px solid #4F46E5;">
            <h4 style="margin-top: 0; color: #1F2937;">Registration Summary</h4>
            <p><strong>👤 Name:</strong> {st.session_state.get('name')}</p>
            <p><strong>🆔 Member ID:</strong> {st.session_state.get('id_member')}</p>
            <p><strong>🎯 Course ID:</strong> {st.session_state.get('course_id')}</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("⬅️ Back to Course Selection"):
                st.session_state.stage = 1
                st.rerun()
        
        with col2:
            if st.button("✅ Confirm Registration", type="primary", use_container_width=True):
                # Process registration
                with st.spinner("Processing your registration..."):
                    result = registrations(st.session_state.get('id_member'), st.session_state.get('course_id'))
                    
                if "successfully" in result.lower():
                    st.balloons()
                    st.success(f"🎉 {result}")
                    st.session_state.stage = 0  # Reset for new registration
                else:
                    st.error(f"❌ {result}")
        
        st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown(create_section_header("My Registration History", "📈", "Track your fitness journey and registration activity"), unsafe_allow_html=True)
    
    # User input for history
    col1, col2 = st.columns([3, 1])
    with col1:
        name_input = st.text_input("Enter your name to view history:", placeholder="Your full name as registered")
    with col2:
        search_button = st.button("🔍 Search", use_container_width=True)
    
    if search_button and name_input:
        with st.spinner("Loading your registration history..."):
            history = historic_registrations(name_input)
            history_count = historic_number_registrations(name_input)
        
        if history:
            # Display metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(create_metric_card("Total Registrations", str(history_count), "📊"), unsafe_allow_html=True)
            with col2:
                st.markdown(create_metric_card("Active Status", "Member", "👤"), unsafe_allow_html=True)
            with col3:
                st.markdown(create_metric_card("Latest Activity", "Recent", "⏰"), unsafe_allow_html=True)
            
            # Registration chart
            chart = create_registration_history_chart(history)
            if chart:
                st.plotly_chart(chart, use_container_width=True)
            
            # Detailed history table
            st.markdown("### 📋 Detailed Registration History")
            
            history_data = []
            for reg in history:
                history_data.append({
                    'Registration ID': reg.registration_id,
                    'Course ID': reg.course_id,
                    'Registration Date': reg.registration_date.strftime('%Y-%m-%d %H:%M'),
                    'Status': '✅ Confirmed'
                })
            
            if history_data:
                st.dataframe(history_data, use_container_width=True)
            
        else:
            st.info("🤷‍♂️ No registration history found for this name. Make sure you've entered the correct name.")
    
    elif not name_input and search_button:
        st.warning("⚠️ Please enter your name to search for registration history.")
