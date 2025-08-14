# Modern Course Management Interface
import streamlit as st
from init_db import engine
from sqlmodel import Session, select, func
from model import Members, Coaches, Accesscards, Registrations, Courses
from utils import add_member, select_course, add_course, delete_course, delete_member, update_members
import pandas as pd
import datetime
from styles import apply_custom_css, create_welcome_card, create_metric_card, create_section_header
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, time

# Apply modern styling
apply_custom_css()

def course_list():
    """Get enhanced course list with additional statistics"""
    with Session(engine) as session:
        stmt = select(Courses)
        results = session.exec(stmt).all()
        data = []
        for row in results:
            # Count registrations for this course
            reg_count = len(session.exec(
                select(Registrations)
                .where(Registrations.course_id == str(row.course_id))
            ).all())
            
            # Get coach name
            coach = session.exec(
                select(Coaches).where(Coaches.coach_id == row.coach_id)
            ).first()
            coach_name = coach.coach_name if coach else "Unknown"
            coach_specialty = coach.specialty if coach else "Unknown"
            
            data.append({
                'course_id': row.course_id,
                'course_name': row.course_name,
                'coach_id': row.coach_id,
                'coach_name': coach_name,
                'coach_specialty': coach_specialty,
                'time_plan': row.time_plan,
                'max_capacity': row.max_capacity,
                'total_participants': reg_count,
                'status': 'Active' if reg_count > 0 else 'Scheduled'
            })
        
        return pd.DataFrame(data)

def create_course_analytics(courses_df):
    """Create analytics charts for courses"""
    if courses_df.empty:
        return None, None
    
    # Course popularity chart
    fig1 = px.bar(
        courses_df.sort_values('total_participants', ascending=True).tail(10),
        x='total_participants',
        y='course_name',
        orientation='h',
        title="Most Popular Courses",
        color='total_participants',
        color_continuous_scale='viridis'
    )
    fig1.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_family="Inter",
        title_font_size=16,
        height=300
    )
    
    # Course status distribution
    status_counts = courses_df['status'].value_counts()
    fig2 = px.pie(
        values=status_counts.values,
        names=status_counts.index,
        title="Course Status Distribution",
        color_discrete_map={'Active': '#10B981', 'Scheduled': '#F59E0B'}
    )
    fig2.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_family="Inter",
        title_font_size=16,
        height=300
    )
    
    return fig1, fig2

def display_course_cards(courses_df):
    """Display courses as modern cards"""
    if courses_df.empty:
        st.warning("No courses found in the system.")
        return
    
    # Pagination for large datasets
    items_per_page = 8
    total_items = len(courses_df)
    total_pages = (total_items - 1) // items_per_page + 1
    
    if 'current_page_courses' not in st.session_state:
        st.session_state.current_page_courses = 1
    
    # Page navigation
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("⬅️ Previous", key="prev_courses") and st.session_state.current_page_courses > 1:
            st.session_state.current_page_courses -= 1
            st.rerun()
    
    with col2:
        st.markdown(f"<div style='text-align: center; font-weight: 600;'>Page {st.session_state.current_page_courses} of {total_pages}</div>", unsafe_allow_html=True)
    
    with col3:
        if st.button("Next ➡️", key="next_courses") and st.session_state.current_page_courses < total_pages:
            st.session_state.current_page_courses += 1
            st.rerun()
    
    # Calculate start and end indices
    start_idx = (st.session_state.current_page_courses - 1) * items_per_page
    end_idx = min(start_idx + items_per_page, total_items)
    
    # Display courses for current page
    page_courses = courses_df.iloc[start_idx:end_idx]
    
    cols = st.columns(2)
    for idx, course in page_courses.iterrows():
        with cols[idx % 2]:
            status_color = "#10B981" if course['status'] == 'Active' else "#F59E0B"
            status_icon = "🟢" if course['status'] == 'Active' else "🟡"
            
            # Format date and time
            try:
                if course['time_plan']:
                    time_plan = pd.to_datetime(course['time_plan'])
                    formatted_date = time_plan.strftime('%B %d, %Y')
                    formatted_time = time_plan.strftime('%H:%M')
                else:
                    formatted_date = "Date TBD"
                    formatted_time = "Time TBD"
            except:
                formatted_date = str(course['time_plan'])
                formatted_time = "Time TBD"
            
            st.markdown(f"""
            <div style="background: white; padding: 1.5rem; border-radius: 16px; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1); margin: 1rem 0;">
                <div style="display: flex; justify-content: space-between; align-items: start;">
                    <div style="flex: 1;">
                        <h3 style="margin: 0; color: #1F2937; font-size: 1.2rem;">🏋️ {course['course_name']}</h3>
                        <p style="color: #6B7280; margin: 0.3rem 0; font-size: 0.9rem;">👨‍🏫 Coach: {course['coach_name']}</p>
                        <p style="color: #6B7280; margin: 0.3rem 0; font-size: 0.9rem;">🏷️ Specialty: {course['coach_specialty']}</p>
                        <p style="color: #6B7280; margin: 0.3rem 0; font-size: 0.9rem;">📅 {formatted_date}</p>
                        <p style="color: #6B7280; margin: 0.3rem 0; font-size: 0.9rem;">⏰ {formatted_time}</p>
                        <p style="color: #6B7280; margin: 0.3rem 0; font-size: 0.9rem;">👥 Max Capacity: {course['max_capacity']}</p>
                        <p style="color: #6B7280; margin: 0.3rem 0; font-size: 0.9rem;">🆔 Course ID: #{course['course_id']}</p>
                        <div style="margin-top: 1rem;">
                            <span style="background: {status_color}; color: white; padding: 0.2rem 0.6rem; border-radius: 15px; font-size: 0.8rem; font-weight: 500;">
                                {status_icon} {course['status']}
                            </span>
                            <span style="background: #F3F4F6; color: #374151; padding: 0.2rem 0.6rem; border-radius: 15px; font-size: 0.8rem; margin-left: 0.5rem;">
                                👥 {course['total_participants']} participants
                            </span>
                        </div>
                    </div>
                    <div style="font-size: 2rem; opacity: 0.3;">🎯</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

def get_coaches_list():
    """Get list of available coaches"""
    with Session(engine) as session:
        coaches = session.exec(select(Coaches)).all()
        return {f"{coach.coach_name} ({coach.specialty})": coach.coach_id for coach in coaches}

# Page header
st.markdown(create_welcome_card(
    "Course Management", 
    "Manage gym courses - schedule new classes, update details, and track participation",
    "Admin"
), unsafe_allow_html=True)

# Initialize session state for course list
if "courses_df" not in st.session_state:
    st.session_state.courses_df = course_list()

# Quick stats
st.markdown(create_section_header("📊 Course Overview", "🎯", "Current course statistics and performance"), unsafe_allow_html=True)

if not st.session_state.courses_df.empty:
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_courses = len(st.session_state.courses_df)
        st.markdown(create_metric_card("Total Courses", str(total_courses), "🎯"), unsafe_allow_html=True)
    
    with col2:
        active_courses = len(st.session_state.courses_df[st.session_state.courses_df['status'] == 'Active'])
        st.markdown(create_metric_card("Active Courses", str(active_courses), "🟢"), unsafe_allow_html=True)
    
    with col3:
        total_participants = st.session_state.courses_df['total_participants'].sum()
        st.markdown(create_metric_card("Total Participants", str(total_participants), "👥"), unsafe_allow_html=True)
    
    with col4:
        avg_participants = st.session_state.courses_df['total_participants'].mean()
        st.markdown(create_metric_card("Avg Per Course", f"{avg_participants:.1f}", "📊"), unsafe_allow_html=True)
    
    # Analytics charts
    st.markdown("### 📈 Course Analytics")
    chart1, chart2 = create_course_analytics(st.session_state.courses_df)
    
    col1, col2 = st.columns(2)
    with col1:
        if chart1:
            st.plotly_chart(chart1, use_container_width=True)
    
    with col2:
        if chart2:
            st.plotly_chart(chart2, use_container_width=True)
    
    # Quick actions
    col1, col2 = st.columns([3, 1])
    with col2:
        st.markdown("### 🔄 Quick Actions")
        if st.button("📊 Refresh Data", use_container_width=True):
            st.session_state.courses_df = course_list()
            st.rerun()
        
        if st.button("📤 Export Courses", use_container_width=True):
            st.download_button(
                label="💾 Download CSV",
                data=st.session_state.courses_df.to_csv(index=False),
                file_name="courses_data.csv",
                mime="text/csv",
                use_container_width=True
            )

# Course cards display
st.markdown(create_section_header("🎯 Current Courses", "🏋️", "Browse and manage scheduled courses"), unsafe_allow_html=True)
display_course_cards(st.session_state.courses_df)

st.markdown("---")

# Management actions
st.markdown(create_section_header("🛠️ Course Management Actions", "⚙️", "Schedule, modify, or remove courses from your system"), unsafe_allow_html=True)

# Action buttons
col1, col2, col3 = st.columns(3)
add_button = col1.button("➕ Schedule New Course", use_container_width=True)
modify_button = col2.button("✏️ Modify Course", use_container_width=True)
delete_button = col3.button("🗑️ Remove Course", use_container_width=True)

# Manage session states
session_states = ['add_form_course', 'modify_form_course', 'delete_form_course']
for state in session_states:
    if state not in st.session_state:
        st.session_state[state] = False

# Reset other forms when one is selected
if add_button:
    st.session_state.add_form_course = True
    st.session_state.modify_form_course = False
    st.session_state.delete_form_course = False

if modify_button:
    st.session_state.add_form_course = False
    st.session_state.modify_form_course = True
    st.session_state.delete_form_course = False

if delete_button:
    st.session_state.add_form_course = False
    st.session_state.modify_form_course = False
    st.session_state.delete_form_course = True

############################################################################
# ADD COURSE FORM
############################################################################
if st.session_state.add_form_course:
    st.markdown('<div style="background: white; padding: 1.5rem; border-radius: 16px; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1); margin: 1rem 0;">', unsafe_allow_html=True)
    with st.form("add_course_form"):
        st.markdown("#### ➕ Schedule New Course")
        st.markdown("Create a new course session with coach assignment and schedule.")
        
        col1, col2 = st.columns(2)
        with col1:
            course_name = st.text_input("Course Name", placeholder="e.g., Morning Yoga, HIIT Training", help="Name of the course/class")
            
            # Get coaches for selection
            coaches = get_coaches_list()
            if coaches:
                coach_selection = st.selectbox("Assign Coach", list(coaches.keys()), help="Select coach for this course")
                selected_coach_id = coaches[coach_selection]
            else:
                st.error("No coaches available. Please add coaches first.")
                selected_coach_id = None
        
        with col2:
            course_date = st.date_input("Course Date", help="When will this course take place?")
            course_time = st.time_input("Course Time", value=time(9, 0), help="Start time for the course")
            max_participants = st.number_input("Max Participants", min_value=5, max_value=50, value=20, step=5, help="Maximum number of participants")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.form_submit_button("❌ Cancel"):
                st.session_state.add_form_course = False
                st.rerun()
        
        with col2:
            course_add = st.form_submit_button("✅ Schedule Course", type="primary")

        if course_add:
            if course_name and selected_coach_id and course_date and course_time:
                with st.spinner("Scheduling new course..."):
                    # Combine date and time into datetime string
                    datetime_str = f"{course_date} {course_time.strftime('%H:%M')}:00"
                    result = add_course(course_name, datetime_str, max_participants, selected_coach_id)
                
                if "successfully" in result.lower():
                    st.balloons()
                    st.success(f"🎉 {result}")
                    st.session_state.courses_df = course_list()
                    st.session_state.add_form_course = False
                    st.rerun()
                else:
                    st.error(f"❌ {result}")
            else:
                st.error("⚠️ Please fill in all required fields.")
    
    st.markdown('</div>', unsafe_allow_html=True)

############################################################################
# DELETE COURSE FORM
############################################################################
if st.session_state.delete_form_course and not st.session_state.courses_df.empty:
    st.markdown('<div style="background: white; padding: 1.5rem; border-radius: 16px; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1); margin: 1rem 0;">', unsafe_allow_html=True)
    with st.form("delete_course_form"):
        st.markdown("#### 🗑️ Remove Course")
        st.markdown("⚠️ **Warning:** This action cannot be undone. The course and all registrations will be permanently removed.")
        
        # Course selection for deletion
        course_options = {}
        for _, course in st.session_state.courses_df.iterrows():
            try:
                formatted_date = pd.to_datetime(course['time_plan']).strftime('%Y-%m-%d %H:%M')
            except:
                formatted_date = str(course['time_plan'])
            
            display_name = f"{course['course_name']} - {formatted_date} ({course['total_participants']} participants)"
            course_options[display_name] = course['course_name']
        
        selected_course_display = st.selectbox("Select Course to Remove", list(course_options.keys()))
        selected_course_name = course_options[selected_course_display]
        
        # Confirmation checkbox
        confirm_delete = st.checkbox("⚠️ I understand this action cannot be undone", help="Check this box to confirm deletion")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.form_submit_button("❌ Cancel"):
                st.session_state.delete_form_course = False
                st.rerun()
        
        with col2:
            course_delete = st.form_submit_button("🗑️ Confirm Removal", type="primary", disabled=not confirm_delete)

        if course_delete and confirm_delete:
            with st.spinner("Removing course from system..."):
                result = delete_course(selected_course_name)
            
            if "removed" in result.lower() or "deleted" in result.lower():
                st.success(f"✅ {result}")
                st.session_state.courses_df = course_list()
                st.session_state.delete_form_course = False
                st.rerun()
            else:
                st.error(f"❌ {result}")
    
    st.markdown('</div>', unsafe_allow_html=True)