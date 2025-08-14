# Modern Coach Management Interface
import streamlit as st
from utils import all_coach_info, add_coach, delete_coach, modify_coach
from styles import apply_custom_css, create_welcome_card, create_metric_card, create_section_header
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Apply modern styling
apply_custom_css()

def create_coach_specialty_chart(coaches_df):
    """Create a pie chart showing coach distribution by specialty"""
    if coaches_df.empty or 'specialty' not in coaches_df.columns:
        return None
    
    specialty_counts = coaches_df['specialty'].value_counts()
    
    fig = px.pie(
        values=specialty_counts.values,
        names=specialty_counts.index,
        title="Coach Distribution by Specialty",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_family="Inter",
        title_font_size=18,
        height=430
    )
    
    return fig

def display_coach_cards(coaches_df):
    """Display coaches as dark glass cards (aligned with Current Courses styling)."""
    if coaches_df.empty:
        st.warning("No coaches found in the system.")
        return

    cols = st.columns(2)
    for idx, coach in coaches_df.iterrows():
        with cols[idx % 2]:
            specialty = coach.get('specialty', 'Unknown') if 'specialty' in coaches_df.columns else 'Unknown'
            specialty_colors = {
                'yoga': '#10B981',
                'pilates': '#8B5CF6',
                'crossfit': '#EF4444',
                'calisthenic': '#F59E0B',
                'body training': '#3B82F6',
                'athletes trainings': '#6366F1',
                'zumba': '#EC4899'
            }
            color = specialty_colors.get(str(specialty).lower(), '#6B7280')

            st.markdown(f"""
            <div style="background: rgba(45, 45, 45, 0.95); padding: 1.5rem; border-radius: 16px; box-shadow: 0 8px 32px rgba(0,0,0,0.3); backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.1); margin: 1rem 0; transition: transform 0.3s ease, box-shadow 0.3s ease; color:#ffffff;">
                <div style="display:flex; justify-content:space-between; align-items:flex-start; gap:1rem;">
                    <div style="flex:1;">
                            <h3 style="margin:0 0 .35rem 0; color:#ffffff; font-size:1.4rem; font-weight:600; letter-spacing:.5px;">{coach['coach_name']}</h3>
                        <p style="color:#cccccc; margin:.25rem 0; font-size:1rem;">🏷️ <strong>Specialty:</strong> {specialty.title()}</p>
                        <p style="color:#cccccc; margin:.25rem 0; font-size:1rem;">🆔 <strong>ID:</strong> #{coach['coach_id']}</p>
                        <div style="margin-top:.75rem; display:flex; gap:.5rem; flex-wrap:wrap;">
                            <span style="background:{color}; color:#ffffff; padding:0.25rem 0.65rem; border-radius:16px; font-size:0.75rem; font-weight:500;">{specialty.title()}</span>
                        </div>
                    </div>
                    <div style="font-size:2rem; opacity:.25;">💪</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# Page header
st.markdown(create_welcome_card(
    "Coach Management", 
    "Manage your fitness coaching team - add, modify, and organize coaches",
    "Admin"
), unsafe_allow_html=True)

# Initialize session state for coach list DataFrame
if "df" not in st.session_state:
    st.session_state.df = all_coach_info()

# Quick stats
st.markdown("### Coach Overview")

if not st.session_state.df.empty:
    col1, col2, col3, col4 = st.columns(4)

    card_style = "background:white; padding:1rem 1rem; border-radius:16px; box-shadow:0 2px 6px rgba(0,0,0,0.05); margin:1rem 0; height:110px; display:flex; align-items:center;"
    inner_style = "display:flex; justify-content:space-between; width:100%; align-items:baseline; gap:.5rem;"
    title_style = "color:#0F172A; margin:0; font-size:1.0rem; font-weight:700;"
    value_style = "color:#374151; font-size:1.3rem; font-weight:600;"

    with col1:
        total_coaches = len(st.session_state.df)
        st.markdown(f"""
        <div style=\"{card_style}\">\n  <div style=\"{inner_style}\">\n    <h4 style=\"{title_style}\">Total Coaches</h4>\n    <span style=\"{value_style}\">{total_coaches}</span>\n  </div>\n</div>
        """, unsafe_allow_html=True)

    with col2:
        specialties = st.session_state.df['specialty'].nunique() if 'specialty' in st.session_state.df.columns else 0
        st.markdown(f"""
        <div style=\"{card_style}\">\n  <div style=\"{inner_style}\">\n    <h4 style=\"{title_style}\">Specialties</h4>\n    <span style=\"{value_style}\">{specialties}</span>\n  </div>\n</div>
        """, unsafe_allow_html=True)

    with col3:
        most_common = "N/A"
        if 'specialty' in st.session_state.df.columns and not st.session_state.df.empty:
            modes = st.session_state.df['specialty'].mode()
            if len(modes) > 0:
                most_common = modes.iloc[0].title()
        st.markdown(f"""
        <div style=\"{card_style}\">\n  <div style=\"{inner_style}\">\n    <h4 style=\"{title_style}\">Top Specialty</h4>\n    <span style=\"{value_style}\">{most_common}</span>\n  </div>\n</div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div style=\"{card_style}\">\n  <div style=\"{inner_style}\">\n    <h4 style=\"{title_style}\">System Status</h4>\n    <span style=\"{value_style}\">Active</span>\n  </div>\n</div>
        """, unsafe_allow_html=True)

    # Coach distribution chart + quick actions
    col_chart, col_actions = st.columns([3, 1])
    with col_chart:
        chart = create_coach_specialty_chart(st.session_state.df)
        if chart:
            st.plotly_chart(chart, use_container_width=True)

    with col_actions:
        st.markdown("### Quick Actions")
        if st.button("📊 Refresh Data", use_container_width=True):
            st.session_state.df = all_coach_info()
            st.rerun()
        if st.button("📤 Export Data", use_container_width=True):
            st.download_button(
                label="💾 Download CSV",
                data=st.session_state.df.to_csv(index=False),
                file_name="coaches_data.csv",
                mime="text/csv",
                use_container_width=True
            )

# Coach cards display
st.markdown("### Current Coaching Team")
display_coach_cards(st.session_state.df)

st.markdown("---")

# Management actions
st.markdown("### Coach Management Actions")

# Action buttons
col1, col2, col3 = st.columns(3)
add_button = col1.button("➕ Add New Coach", use_container_width=True)
modify_button = col2.button("✏️ Modify Coach", use_container_width=True)
delete_button = col3.button("🗑️ Remove Coach", use_container_width=True)

# Manage session states
session_states = ['add_form_coach', 'modify_form_coach', 'delete_form_coach']
for state in session_states:
    if state not in st.session_state:
        st.session_state[state] = False

# Reset other forms when one is selected
if add_button:
    st.session_state.add_form_coach = True
    st.session_state.modify_form_coach = False
    st.session_state.delete_form_coach = False

if modify_button:
    st.session_state.add_form_coach = False
    st.session_state.modify_form_coach = True
    st.session_state.delete_form_coach = False

if delete_button:
    st.session_state.add_form_coach = False
    st.session_state.modify_form_coach = False
    st.session_state.delete_form_coach = True

############################################################################
# ADD COACH FORM
############################################################################
if st.session_state.add_form_coach:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    with st.form("add_form", clear_on_submit=True):
        st.markdown("#### ➕ Add New Coach")
        st.markdown("Fill in the details to add a new coach to your team.")
        
        col1, col2 = st.columns(2)
        with col1:
            c_name = st.text_input("Coach Name", placeholder="Enter full name", help="Full name of the new coach")
        
        with col2:
            specialty_list = ["Select Specialty", "yoga", "pilates", "crossfit", "calisthenic", "body training", "athletes trainings", "zumba"]
            selected_specialty = st.selectbox("Specialty", specialty_list, help="Choose the coach's area of expertise")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.form_submit_button("❌ Cancel"):
                st.session_state.add_form_coach = False
                st.rerun()
        
        with col2:
            coach_add = st.form_submit_button("✅ Add Coach", type="primary")

        if coach_add:
            if c_name and selected_specialty != "Select Specialty":
                with st.spinner("Adding new coach..."):
                    success, message = add_coach(c_name, selected_specialty)
                
                if success:
                    st.balloons()
                    st.success(f"🎉 {message}")
                    st.session_state.df = all_coach_info()
                    st.session_state.add_form_coach = False
                    st.rerun()
                else:
                    st.error(f"❌ {message}")
            else:
                st.error("⚠️ Please fill in all required fields.")
    
    st.markdown('</div>', unsafe_allow_html=True)

############################################################################
# DELETE COACH FORM
############################################################################
if st.session_state.delete_form_coach and not st.session_state.df.empty:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    with st.form("delete_form"):
        st.markdown("#### 🗑️ Remove Coach")
        st.markdown("⚠️ **Warning:** This action cannot be undone. The coach will be permanently removed from the system.")
        
        # Coach selection for deletion
        coach_options = {}
        for _, coach in st.session_state.df.iterrows():
            display_name = f"{coach['coach_name']} (ID: #{coach['coach_id']}) - {coach['specialty'].title()}"
            coach_options[display_name] = coach['coach_id']
        
        selected_coach_display = st.selectbox("Select Coach to Remove", list(coach_options.keys()))
        selected_coach_id = coach_options[selected_coach_display]
        
        # Confirmation checkbox
        confirm_delete = st.checkbox("⚠️ I understand this action cannot be undone", help="Check this box to confirm deletion")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.form_submit_button("❌ Cancel"):
                st.session_state.delete_form_coach = False
                st.rerun()
        
        with col2:
            del_coach = st.form_submit_button("🗑️ Confirm Removal", type="primary", disabled=not confirm_delete)

        if del_coach and confirm_delete:
            with st.spinner("Removing coach from system..."):
                success, message = delete_coach(selected_coach_id)
            
            if success:
                st.success(f"✅ {message}")
                st.session_state.df = all_coach_info()
                st.session_state.delete_form_coach = False
                st.rerun()
            else:
                st.error(f"❌ {message}")
    
    st.markdown('</div>', unsafe_allow_html=True)