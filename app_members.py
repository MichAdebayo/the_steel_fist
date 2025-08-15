import streamlit as st
from utils import registrations, historic_number_registrations, historic_registrations
from init_db import engine
from sqlmodel import Session, select
import pandas as pd
from model import Courses, Registrations
from styles import apply_custom_css, create_welcome_card, create_metric_card, create_section_header
import plotly.express as px


# Apply styling
apply_custom_css()
# Brand hover styling for buttons (applies site-wide; ensures Continue hover matches progress bar color)
st.markdown("""
<style>
/* Base brand color (progress bar color) */
:root { --brand-color: hsl(350, 98%, 64%); }

/* Default & primary buttons */
.stButton > button, .stButton button {
    transition: background .18s ease, color .18s ease, border-color .18s ease;
    border: 1px solid transparent;
}
.stButton > button:hover,
.stButton > button:focus,
.stButton > button:active,
.stButton > button:focus-visible,
.stButton > button[kind="primary"]:hover,
.stButton > button[kind="primary"]:focus,
.stButton > button[kind="primary"]:active {
    background: var(--brand-color) !important;
    background-image: none !important;
    color: #ffffff !important;
    border-color: var(--brand-color) !important;
    box-shadow: 0 0 0 2px rgba(255,255,255,0.15);
    filter: brightness(1.02);
}
</style>
""", unsafe_allow_html=True)

def courses_list():
    """
    Retrieves and processes a list of available courses from the database.

    This function queries the database to fetch all courses, calculates their current registration count, 
    and determines their availability status. It returns a pandas DataFrame with comprehensive course information.

    Returns:
        pd.DataFrame: A DataFrame containing detailed information about each course.
    """
    with Session(engine) as session:
        stmt = select(Courses)
        results = session.exec(stmt).all()
        data = []
        for row in results:
            # Count current registrations
            reg_stmt = select(Registrations).where(Registrations.course_id == str(row.course_id))
            reg_results = session.exec(reg_stmt).all()
            reg_count = len(reg_results)
            
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
    """Renders course information as interactive visual cards in a two-column layout.

    This function takes a DataFrame of courses and displays each course as a visually appealing card. 
    The cards show course details like name, coach ID, time plan, registration status, and capacity.

    Args:
        courses_df (pd.DataFrame): A DataFrame containing course information with columns 
                                   including course_name, coach_id, time_plan, current_registrations, 
                                   max_capacity, and availability.
    """
    if courses_df.empty:
        st.warning("No courses available at the moment.")
        return

    cols = st.columns(2)
    for idx, course in courses_df.iterrows():
        with cols[idx % 2]:
            capacity_percentage = (course['current_registrations'] / course['max_capacity']) * 100 if course['max_capacity'] else 0
            course_name = course['course_name']
            coach_id = course['coach_id']
            time_plan = course['time_plan']
            current_reg = course['current_registrations']
            max_cap = course['max_capacity']
            status_icon = "🟢" if course['availability'] == 'Available' else "⚪"
            status_color = "#10B981" if course['availability'] == 'Available' else "#EF4444"

            if capacity_percentage < 80:
                progress_color = "#10B981"
            elif capacity_percentage < 100:
                progress_color = "#F59E0B"
            else:
                progress_color = "#EF4444"

            st.markdown(f"""
            <div style="background: rgba(45,45,45,0.95); padding:1.5rem; border-radius:16px; box-shadow:0 8px 32px rgba(0,0,0,0.3); backdrop-filter:blur(10px); border:1px solid rgba(255,255,255,0.1); margin:1rem 0; color:#ffffff;">
                <div style="display:flex; justify-content:space-between; align-items:flex-start; gap:1rem;">
                    <div style="flex:1;">
                        <h3 style="margin:0 0 .5rem 0; font-size:1.4rem; font-weight:600; letter-spacing:.5px;">{course_name}</h3>
                        <p style="color:#cccccc; margin:.25rem 0; font-size:1rem;">🆔 Coach ID: {coach_id}</p>
                        <p style="color:#cccccc; margin:.25rem 0; font-size:1rem;">📅 {time_plan}</p>
                        <div style="margin-top:.75rem; display:flex; flex-wrap:wrap; gap:.5rem; align-items:center;">
                            <span style="background:{status_color}; color:#ffffff; padding:0.25rem 0.65rem; border-radius:16px; font-size:.7rem; font-weight:500; display:inline-flex; gap:.35rem; align-items:center;">{status_icon} {course['availability']}</span>
                            <span style="background:rgba(75,75,75,0.8); color:#cccccc; padding:0.25rem 0.65rem; border-radius:16px; font-size:.7rem;">{current_reg}/{max_cap} registered</span>
                        </div>
                        <div style="margin-top:.9rem;">
                            <div style="background:rgba(255,255,255,0.12); border-radius:10px; height:8px;">
                                <div style="background:{progress_color}; width:{capacity_percentage}%; height:100%; border-radius:10px;"></div>
                            </div>
                        </div>
                    </div>
                    <div style="font-size:2.25rem; opacity:.25;">🏋️</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

def create_registration_history_chart(registrations_data):
    """Creates a line chart visualizing monthly registration activity.

    This function processes registration data to generate a monthly trend chart of registrations. 
    It converts registration dates to a monthly format and plots the number of registrations per month.

    Args:
        registrations_data (list): A list of registration objects containing registration dates and course IDs.

    Returns:
        plotly.graph_objs._figure.Figure or None: A Plotly line chart showing registration trends, 
        or None if no registration data is available.
    """
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
tab1, tab2 = st.tabs(["Register for Courses", "My Activity"])

with tab1:
    st.markdown(create_section_header("Available Courses", "", "Browse and register for available fitness classes"), unsafe_allow_html=True)
    
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
    st.markdown(create_section_header("Quick Registration", "", "Register for a course in 3 simple steps"), unsafe_allow_html=True)
    
    # Progress tracking
    if 'stage' not in st.session_state:
        st.session_state.stage = 0
    
    progress_text = f"Step {st.session_state.stage + 1} of 3"
    progress_value = (st.session_state.stage + 1) / 3
    st.progress(progress_value, text=progress_text)
    
    def process_form():
        st.session_state.form_submitted = True
    
    if st.session_state.stage == 0:
        st.markdown('<div style="background: white; padding: 1.5rem; border-radius: 16px; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1); margin: 1rem 0;">', unsafe_allow_html=True)
        with st.form("personal_details", clear_on_submit=False):
            st.markdown("#### Personal Information")
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("Full Name", placeholder="Enter your full name", help="Your registered name in the system")
            with col2:
                id_member = st.text_input("Member ID", placeholder="Enter your member ID", help="Your unique member identification number")
            
            submitted = st.form_submit_button("Continue", use_container_width=True)
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
        st.markdown('<div style="background: white; padding: 1.5rem; border-radius: 16px; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1); margin: 1rem 0;">', unsafe_allow_html=True)
        with st.form("choose_program"):
            st.markdown("#### Choose Your Course")
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
                submitted = st.form_submit_button("Continue", type="primary")
        st.markdown('</div>', unsafe_allow_html=True)

        if submitted and course_id:
            st.session_state.course_id = course_id
            st.session_state.stage = 2
            st.success("✅ Course selected!")
            st.rerun()

    elif st.session_state.stage == 2:
        st.markdown('<div style="background: white; padding: 1.5rem; border-radius: 16px; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1); margin: 1rem 0;">', unsafe_allow_html=True)
        st.markdown("#### Review Your Registration")

        # Display summary
        st.markdown(f"""
        <div style=\"background: #F8FAFC; padding: 1.5rem; border-radius: 12px; border-left: 4px solid #4F46E5;\">
            <h4 style=\"margin-top: 0; color: #1F2937;\">Registration Summary</h4>
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
    # Left-aligned header & description (override create_section_header layout for tighter alignment)
    st.markdown("""
    <div style='margin: 1.5rem 0 1rem 0;'>
        <div style='font-size:1.5rem; font-weight:600; color:#F1F5F9; margin:0; letter-spacing:.5px;'>My Registration History</div>
        <div style='color:#CBD5E1; font-size:0.9rem; margin-top:.35rem;'>Track your fitness journey and registration activity</div>
    </div>
    """, unsafe_allow_html=True)
    
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
