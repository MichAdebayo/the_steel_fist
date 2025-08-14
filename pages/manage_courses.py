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
    """Create analytics charts for courses (updated sizes & axis labels)."""
    if courses_df.empty:
        return None, None

    # Prepare a display-friendly course name (capitalize first letter only to preserve acronyms like HIIT)
    courses_display = courses_df.copy()
    courses_display['course_name_display'] = courses_display['course_name'].apply(
        lambda s: s[:1].upper() + s[1:] if isinstance(s, str) and s else s
    )

    # Course popularity chart (larger, custom axis titles)
    fig1 = px.bar(
        courses_display.sort_values('total_participants', ascending=True).tail(10),
        x='total_participants',
        y='course_name_display',
        orientation='h',
        title="Most Popular Courses",
        color='total_participants',
        color_continuous_scale='viridis'
    )
    fig1.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_family="Inter",
        title_font_size=18,
        height=430,
        xaxis_title="Total participants",
    yaxis_title="Course name"
    )
    # Set readable legend/color bar title
    fig1.update_layout(coloraxis_colorbar=dict(title="Total participants"))

    # Course status distribution (larger pie chart)
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
        title_font_size=18,
        height=430
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

            # Dark glass style with icons & enlarged title + status dot
            status_icon = "🟢" if course['status'] == 'Active' else "⚪"
            st.markdown(f"""
            <div style="background: rgba(45, 45, 45, 0.95); padding: 1.5rem; border-radius: 16px; box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3); backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.1); margin: 1rem 0; transition: transform 0.3s ease, box-shadow 0.3s ease; color: #ffffff;">
                <div style="display: flex; justify-content: space-between; align-items: start; gap:1rem;">
                    <div style="flex: 1;">
                        <h3 style="margin: 0 0 .35rem 0; color: #ffffff; font-size: 1.5rem; font-weight:600; letter-spacing:.5px;">{course['course_name']}</h3>
                        <p style="color: #cccccc; margin: 0.25rem 0; font-size: 0.9rem;">👨‍🏫 <strong>Coach:</strong> {course['coach_name']}</p>
                        <p style="color: #cccccc; margin: 0.25rem 0; font-size: 0.9rem;">🏷️ <strong>Specialty:</strong> {course['coach_specialty']}</p>
                        <p style="color: #cccccc; margin: 0.25rem 0; font-size: 0.9rem;">📅 <strong>Date:</strong> {formatted_date}</p>
                        <p style="color: #cccccc; margin: 0.25rem 0; font-size: 0.9rem;">⏰ <strong>Time:</strong> {formatted_time}</p>
                        <p style="color: #cccccc; margin: 0.25rem 0; font-size: 0.9rem;">👥 <strong>Capacity:</strong> {course['max_capacity']}</p>
                        <p style="color: #cccccc; margin: 0.25rem 0; font-size: 0.9rem;">🆔 <strong>ID:</strong> #{course['course_id']}</p>
                        <div style="margin-top: .75rem; display:flex; flex-wrap:wrap; gap:.5rem; align-items:center;">
                            <span style="background: {status_color}; color: white; padding: 0.25rem 0.65rem; border-radius: 16px; font-size: 0.75rem; font-weight: 500; display:inline-flex; align-items:center; gap:.35rem;">
                                <span>{status_icon}</span> {course['status']}
                            </span>
                            <span style="background: rgba(75, 75, 75, 0.8); color: #cccccc; padding: 0.25rem 0.65rem; border-radius: 16px; font-size: 0.75rem;">
                                {course['total_participants']} participants
                            </span>
                        </div>
                    </div>
                    <div style="font-size: 2rem; opacity: 0.25;">🏋️</div>
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

st.markdown("### Course Overview")

# Rebuild metrics block cleanly
if not st.session_state.courses_df.empty:
    col1, col2, col3, col4 = st.columns(4)

    card_style = "background:white; padding:1rem 1rem; border-radius:16px; box-shadow:0 2px 6px rgba(0,0,0,0.05); margin:1rem 0; height:110px; display:flex; align-items:center;"
    inner_style = "display:flex; justify-content:space-between; width:100%; align-items:baseline; gap:.5rem;"
    title_style = "color:#0F172A; margin:0; font-size:1.0rem; font-weight:700;"
    value_style = "color:#374151; font-size:1.3rem; font-weight:600;"

    with col1:
        total_courses = len(st.session_state.courses_df)
        st.markdown(f"""
        <div style=\"{card_style}\">\n  <div style=\"{inner_style}\">\n    <h4 style=\"{title_style}\">Total Courses</h4>\n    <span style=\"{value_style}\">{total_courses}</span>\n  </div>\n</div>
        """, unsafe_allow_html=True)

    with col2:
        active_courses = len(st.session_state.courses_df[st.session_state.courses_df['status'] == 'Active'])
        st.markdown(f"""
        <div style=\"{card_style}\">\n  <div style=\"{inner_style}\">\n    <h4 style=\"{title_style}\">Active Courses</h4>\n    <span style=\"{value_style}\">{active_courses}</span>\n  </div>\n</div>
        """, unsafe_allow_html=True)

    with col3:
        total_participants = st.session_state.courses_df['total_participants'].sum()
        st.markdown(f"""
        <div style=\"{card_style}\">\n  <div style=\"{inner_style}\">\n    <h4 style=\"{title_style}\">Total Participants</h4>\n    <span style=\"{value_style}\">{total_participants}</span>\n  </div>\n</div>
        """, unsafe_allow_html=True)

    with col4:
        avg_participants = st.session_state.courses_df['total_participants'].mean()
        st.markdown(f"""
        <div style=\"{card_style}\">\n  <div style=\"{inner_style}\">\n    <h4 style=\"{title_style}\">Avg Per Course</h4>\n    <span style=\"{value_style}\">{avg_participants:.1f}</span>\n  </div>\n</div>
        """, unsafe_allow_html=True)
    
    # Analytics charts
    st.markdown("### Course Analytics")
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
        st.markdown("### Quick Actions")
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
st.markdown("### Current Courses")
display_course_cards(st.session_state.courses_df)

st.markdown("---")

# Management actions
st.markdown("### Course Management Actions")

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