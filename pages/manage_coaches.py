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
        title_font_size=16,
        height=300
    )
    
    return fig

def display_coach_cards(coaches_df):
    """Display coaches as modern cards"""
    if coaches_df.empty:
        st.warning("No coaches found in the system.")
        return
    
    cols = st.columns(2)
    for idx, coach in coaches_df.iterrows():
        with cols[idx % 2]:
            # Check if specialty column exists
            specialty = coach.get('specialty', 'Unknown') if 'specialty' in coaches_df.columns else 'Unknown'
            
            # Specialty color mapping
            specialty_colors = {
                'yoga': '#10B981',
                'pilates': '#8B5CF6', 
                'crossfit': '#EF4444',
                'calisthenic': '#F59E0B',
                'body training': '#3B82F6',
                'athletes trainings': '#6366F1',
                'zumba': '#EC4899'
            }
            
            color = specialty_colors.get(specialty.lower(), '#6B7280')
            
            st.markdown(f"""
            <div class="coach-card">
                <div style="display: flex; justify-content: space-between; align-items: start;">
                    <div>
                        <h3 style="margin: 0; color: var(--text-high, #0F172A); font-size: 1.3rem;">👨‍🏫 {coach['coach_name']}</h3>
                        <p style="color: #6B7280; margin: 0.5rem 0; font-size: 0.9rem;">Coach ID: #{coach['coach_id']}</p>
                        <span style="background: {color}; color: white; padding: 0.3rem 0.8rem; border-radius: 20px; font-size: 0.8rem; font-weight: 500;">
                            🎯 {specialty.title()}
                        </span>
                    </div>
                    <div style="font-size: 2.5rem; opacity: 0.3;">💪</div>
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
st.markdown(create_section_header("📊 Coach Overview", "👥", "Current coaching team statistics"), unsafe_allow_html=True)

if not st.session_state.df.empty:
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_coaches = len(st.session_state.df)
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-radius: 16px; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1); text-align: center; margin: 1rem 0; height: 140px; display: flex; flex-direction: column; justify-content: center;">
            <div style="font-size: 2rem; margin-bottom: 1rem;">👨‍🏫</div>
            <h4 style="color: var(--text-high, #0F172A); margin: 0; font-size: 1.1rem; line-height: 1.2;">Total Coaches</h4>
            <p style="color: #6B7280; margin: 0.5rem 0 0 0; font-size: 0.9rem; font-weight: 500;">{}</p>
        </div>
        """.format(str(total_coaches)), unsafe_allow_html=True)
    
    with col2:
        if 'specialty' in st.session_state.df.columns:
            specialties = st.session_state.df['specialty'].nunique()
        else:
            specialties = 0
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-radius: 16px; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1); text-align: center; margin: 1rem 0; height: 140px; display: flex; flex-direction: column; justify-content: center;">
            <div style="font-size: 2rem; margin-bottom: 1rem;">🎯</div>
            <h4 style="color: var(--text-high, #0F172A); margin: 0; font-size: 1.1rem; line-height: 1.2;">Specialties</h4>
            <p style="color: #6B7280; margin: 0.5rem 0 0 0; font-size: 0.9rem; font-weight: 500;">{}</p>
        </div>
        """.format(str(specialties)), unsafe_allow_html=True)
    
    with col3:
        if 'specialty' in st.session_state.df.columns and not st.session_state.df.empty:
            most_common = st.session_state.df['specialty'].mode().iloc[0] if len(st.session_state.df['specialty'].mode()) > 0 else "N/A"
        else:
            most_common = "N/A"
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-radius: 16px; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1); text-align: center; margin: 1rem 0; height: 140px; display: flex; flex-direction: column; justify-content: center;">
            <div style="font-size: 2rem; margin-bottom: 1rem;">⭐</div>
            <h4 style="color: var(--text-high, #0F172A); margin: 0; font-size: 1.1rem; line-height: 1.2;">Popular Specialty</h4>
            <p style="color: #6B7280; margin: 0.5rem 0 0 0; font-size: 0.9rem; font-weight: 500;">{}</p>
        </div>
        """.format(most_common.title() if most_common != "N/A" else "N/A"), unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-radius: 16px; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1); text-align: center; margin: 1rem 0; height: 140px; display: flex; flex-direction: column; justify-content: center;">
            <div style="font-size: 2rem; margin-bottom: 1rem;">✅</div>
            <h4 style="color: var(--text-high, #0F172A); margin: 0; font-size: 1.1rem; line-height: 1.2;">System Status</h4>
            <p style="color: #6B7280; margin: 0.5rem 0 0 0; font-size: 0.9rem; font-weight: 500;">Active</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Coach distribution chart
    col1, col2 = st.columns([2, 1])
    with col1:
        chart = create_coach_specialty_chart(st.session_state.df)
        if chart:
            st.plotly_chart(chart, use_container_width=True)
    
    with col2:
        st.markdown("### 🔄 Quick Actions")
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
st.markdown(create_section_header("👥 Current Coaching Team", "🏋️‍♂️", "Browse and manage individual coaches"), unsafe_allow_html=True)
display_coach_cards(st.session_state.df)

st.markdown("---")

# Management actions
st.markdown(create_section_header("🛠️ Coach Management Actions", "⚙️", "Add, modify, or remove coaches from your team"), unsafe_allow_html=True)

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
# MODIFY COACH FORM
############################################################################
if st.session_state.modify_form_coach and not st.session_state.df.empty:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    with st.form("modify_form"):
        st.markdown("#### ✏️ Modify Coach Information")
        st.markdown("Update coach details and specialty information.")
        
        # Coach selection
        coach_options = {}
        for _, coach in st.session_state.df.iterrows():
            display_name = f"{coach['coach_name']} (ID: #{coach['coach_id']}) - {coach['specialty'].title()}"
            coach_options[display_name] = coach['coach_id']
        
        selected_coach_display = st.selectbox("Select Coach to Modify", list(coach_options.keys()))
        selected_coach_id = coach_options[selected_coach_display]
        
        # Get current coach info
        current_coach = st.session_state.df[st.session_state.df['coach_id'] == selected_coach_id].iloc[0]
        
        col1, col2 = st.columns(2)
        with col1:
            new_name = st.text_input("New Name", value=current_coach['coach_name'], help="Update coach's name")
        
        with col2:
            specialty_list = ["yoga", "pilates", "crossfit", "calisthenic", "body training", "athletes trainings", "zumba"]
            current_index = specialty_list.index(current_coach['specialty']) if current_coach['specialty'] in specialty_list else 0
            new_specialty = st.selectbox("New Specialty", specialty_list, index=current_index, help="Update coach's specialty")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.form_submit_button("❌ Cancel"):
                st.session_state.modify_form_coach = False
                st.rerun()
        
        with col2:
            mod_coach = st.form_submit_button("✅ Update Coach", type="primary")

        if mod_coach:
            if new_name and new_specialty:
                with st.spinner("Updating coach information..."):
                    success, message = modify_coach(selected_coach_id, new_name, new_specialty)
                
                if success:
                    st.success(f"✅ {message}")
                    st.session_state.df = all_coach_info()
                    st.session_state.modify_form_coach = False
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