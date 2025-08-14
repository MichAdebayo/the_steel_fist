# Modern Member Management Interface
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

# Apply modern styling
apply_custom_css()

def member_list():
    """Get enhanced member list with additional statistics"""
    with Session(engine) as session:
        stmt = select(Members)
        results = session.exec(stmt).all()
        data = []
        for row in results:
            # Count member's registrations
            reg_count = len(session.exec(
                select(Registrations)
                .where(Registrations.member_id == str(row.member_id))
            ).all())
            
            data.append({
                'member_id': row.member_id,
                'member_name': row.member_name,
                'email': row.email,
                'access_card_id': row.access_card_id,
                'total_registrations': reg_count,
                'status': 'Active' if reg_count > 0 else 'Inactive'
            })
        
        return pd.DataFrame(data)

def create_member_activity_chart(members_df):
    """Create a chart showing member activity distribution"""
    if members_df.empty or 'status' not in members_df.columns:
        return None
    
    activity_counts = members_df['status'].value_counts()
    
    fig = px.pie(
        values=activity_counts.values,
        names=activity_counts.index,
        title="Member Activity Status",
        color_discrete_map={'Active': '#10B981', 'Inactive': '#6B7280'}
    )
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_family="Inter",
        title_font_size=16,
        height=300
    )
    
    return fig

def display_member_cards(members_df):
    """Display members as modern cards"""
    if members_df.empty:
        st.warning("No members found in the system.")
        return
    
    # Pagination for large datasets
    items_per_page = 10
    total_items = len(members_df)
    total_pages = (total_items - 1) // items_per_page + 1
    
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 1
    
    # Page navigation
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("⬅️ Previous") and st.session_state.current_page > 1:
            st.session_state.current_page -= 1
            st.rerun()
    
    with col2:
        st.markdown(f"<div style='text-align: center; font-weight: 600;'>Page {st.session_state.current_page} of {total_pages}</div>", unsafe_allow_html=True)
    
    with col3:
        if st.button("Next ➡️") and st.session_state.current_page < total_pages:
            st.session_state.current_page += 1
            st.rerun()
    
    # Calculate start and end indices
    start_idx = (st.session_state.current_page - 1) * items_per_page
    end_idx = min(start_idx + items_per_page, total_items)
    
    # Display members for current page
    page_members = members_df.iloc[start_idx:end_idx]
    
    cols = st.columns(2)
    for idx, member in page_members.iterrows():
        with cols[idx % 2]:
            # Handle missing status column
            member_status = member.get('status', 'Unknown') if 'status' in member else 'Unknown'
            status_color = "#10B981" if member_status == 'Active' else "#6B7280"
            status_icon = "🟢" if member_status == 'Active' else "⚪"
            
            st.markdown(f"""
            <div class="metric-card">
                <div style="display: flex; justify-content: space-between; align-items: start;">
                    <div style="flex: 1;">
                        <h3 style="margin: 0; color: #1F2937; font-size: 1.2rem;">👤 {member['member_name']}</h3>
                        <p style="color: #6B7280; margin: 0.3rem 0; font-size: 0.9rem;">📧 {member['email']}</p>
                        <p style="color: #6B7280; margin: 0.3rem 0; font-size: 0.9rem;">🆔 Member ID: #{member['member_id']}</p>
                        <p style="color: #6B7280; margin: 0.3rem 0; font-size: 0.9rem;">🎫 Access Card: #{member['access_card_id']}</p>
                        <div style="margin-top: 1rem;">
                            <span style="background: {status_color}; color: white; padding: 0.2rem 0.6rem; border-radius: 15px; font-size: 0.8rem; font-weight: 500;">
                                {status_icon} {member_status}
                            </span>
                            <span style="background: #F3F4F6; color: #374151; padding: 0.2rem 0.6rem; border-radius: 15px; font-size: 0.8rem; margin-left: 0.5rem;">
                                📊 {member['total_registrations']} registrations
                            </span>
                        </div>
                    </div>
                    <div style="font-size: 2rem; opacity: 0.3;">🏃‍♂️</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# Page header
st.markdown(create_welcome_card(
    "Member Management", 
    "Manage gym members - add new members, update information, and track activity",
    "Admin"
), unsafe_allow_html=True)

# Initialize session state for member list
if "df" not in st.session_state:
    st.session_state.df = member_list()

# Quick stats
st.markdown(create_section_header("📊 Member Overview", "👥", "Current membership statistics and activity"), unsafe_allow_html=True)

if not st.session_state.df.empty:
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_members = len(st.session_state.df)
        st.markdown(create_metric_card("Total Members", str(total_members), "👥"), unsafe_allow_html=True)
    
    with col2:
        if 'status' in st.session_state.df.columns:
            active_members = len(st.session_state.df[st.session_state.df['status'] == 'Active'])
        else:
            active_members = 0
        st.markdown(create_metric_card("Active Members", str(active_members), "🟢"), unsafe_allow_html=True)
    
    with col3:
        if 'total_registrations' in st.session_state.df.columns:
            avg_registrations = st.session_state.df['total_registrations'].mean()
        else:
            avg_registrations = 0
        st.markdown(create_metric_card("Avg Registrations", f"{avg_registrations:.1f}", "📊"), unsafe_allow_html=True)
    
    with col4:
        if 'status' in st.session_state.df.columns:
            active_members = len(st.session_state.df[st.session_state.df['status'] == 'Active'])
        else:
            active_members = 0
        engagement_rate = (active_members / total_members * 100) if total_members > 0 else 0
        st.markdown(create_metric_card("Engagement Rate", f"{engagement_rate:.1f}%", "⚡"), unsafe_allow_html=True)
    
    # Charts and quick actions
    col1, col2 = st.columns([2, 1])
    with col1:
        chart = create_member_activity_chart(st.session_state.df)
        if chart:
            st.plotly_chart(chart, use_container_width=True)
    
    with col2:
        st.markdown("### 🔄 Quick Actions")
        if st.button("📊 Refresh Data", use_container_width=True):
            st.session_state.df = member_list()
            st.rerun()
        
        if st.button("📤 Export Members", use_container_width=True):
            st.download_button(
                label="💾 Download CSV",
                data=st.session_state.df.to_csv(index=False),
                file_name="members_data.csv",
                mime="text/csv",
                use_container_width=True
            )

# Member cards display
st.markdown(create_section_header("👥 Current Members", "🏃‍♂️", "Browse and manage individual member accounts"), unsafe_allow_html=True)
display_member_cards(st.session_state.df)

st.markdown("---")

# Management actions
st.markdown(create_section_header("🛠️ Member Management Actions", "⚙️", "Add, modify, or remove members from your system"), unsafe_allow_html=True)

# Action buttons
col1, col2, col3 = st.columns(3)
add_button = col1.button("➕ Add New Member", use_container_width=True)
modify_button = col2.button("✏️ Modify Member", use_container_width=True)
delete_button = col3.button("🗑️ Remove Member", use_container_width=True)

# Manage session states
session_states = ['add_form_member', 'modify_form_member', 'delete_form_member']
for state in session_states:
    if state not in st.session_state:
        st.session_state[state] = False

# Reset other forms when one is selected
if add_button:
    st.session_state.add_form_member = True
    st.session_state.modify_form_member = False
    st.session_state.delete_form_member = False

if modify_button:
    st.session_state.add_form_member = False
    st.session_state.modify_form_member = True
    st.session_state.delete_form_member = False

if delete_button:
    st.session_state.add_form_member = False
    st.session_state.modify_form_member = False
    st.session_state.delete_form_member = True

############################################################################
# ADD MEMBER FORM
############################################################################
if st.session_state.add_form_member:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    with st.form("add_form"):
        st.markdown("#### ➕ Add New Member")
        st.markdown("Register a new gym member with access card.")
        
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Full Name", placeholder="Enter member's full name", help="Member's complete name")
            access = st.text_input("Access Card Number", placeholder="6-digit access card number", help="Unique 6-digit access card identifier")
        
        with col2:
            mail = st.text_input("Email Address", placeholder="member@email.com", help="Member's email address for communication")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.form_submit_button("❌ Cancel"):
                st.session_state.add_form_member = False
                st.rerun()
        
        with col2:
            member_add = st.form_submit_button("✅ Add Member", type="primary")

        if member_add:
            if name and mail and access:
                with st.spinner("Adding new member..."):
                    result = add_member(name, mail, access)
                
                if "successful" in result.lower():
                    st.balloons()
                    st.success(f"🎉 {result}")
                    st.session_state.df = member_list()
                    st.session_state.add_form_member = False
                    st.rerun()
                else:
                    st.error(f"❌ {result}")
            else:
                st.error("⚠️ Please fill in all required fields.")
    
    st.markdown('</div>', unsafe_allow_html=True)

############################################################################
# MODIFY MEMBER FORM
############################################################################
if st.session_state.modify_form_member and not st.session_state.df.empty:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    with st.form("modify_form"):
        st.markdown("#### ✏️ Modify Member Information")
        st.markdown("Update member details and contact information.")
        
        # Member selection
        member_options = {}
        for _, member in st.session_state.df.iterrows():
            display_name = f"{member['member_name']} (ID: #{member['member_id']}) - {member['email']}"
            member_options[display_name] = member['member_id']
        
        selected_member_display = st.selectbox("Select Member to Modify", list(member_options.keys()))
        selected_member_id = member_options[selected_member_display]
        
        # Get current member info
        current_member = st.session_state.df[st.session_state.df['member_id'] == selected_member_id].iloc[0]
        
        col1, col2 = st.columns(2)
        with col1:
            new_name = st.text_input("New Name", value=current_member['member_name'], help="Update member's name")
        
        with col2:
            new_mail = st.text_input("New Email", value=current_member['email'], help="Update member's email address")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.form_submit_button("❌ Cancel"):
                st.session_state.modify_form_member = False
                st.rerun()
        
        with col2:
            modify_member = st.form_submit_button("✅ Update Member", type="primary")

        if modify_member:
            if new_name and new_mail:
                with st.spinner("Updating member information..."):
                    result = update_members(selected_member_id, new_name, new_mail)
                
                if "successful" in result.lower():
                    st.success(f"✅ {result}")
                    st.session_state.df = member_list()
                    st.session_state.modify_form_member = False
                    st.rerun()
                else:
                    st.error(f"❌ {result}")
            else:
                st.error("⚠️ Please fill in all required fields.")
    
    st.markdown('</div>', unsafe_allow_html=True)

############################################################################
# DELETE MEMBER FORM
############################################################################
if st.session_state.delete_form_member and not st.session_state.df.empty:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    with st.form("delete_form"):
        st.markdown("#### 🗑️ Remove Member")
        st.markdown("⚠️ **Warning:** This action cannot be undone. The member and all associated data will be permanently removed.")
        
        # Member selection for deletion
        member_options = {}
        for _, member in st.session_state.df.iterrows():
            display_name = f"{member['member_name']} (ID: #{member['member_id']}) - {member['total_registrations']} registrations"
            member_options[display_name] = member['member_name']
        
        selected_member_display = st.selectbox("Select Member to Remove", list(member_options.keys()))
        selected_member_name = member_options[selected_member_display]
        
        # Confirmation checkbox
        confirm_delete = st.checkbox("⚠️ I understand this action cannot be undone", help="Check this box to confirm deletion")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.form_submit_button("❌ Cancel"):
                st.session_state.delete_form_member = False
                st.rerun()
        
        with col2:
            member_delete = st.form_submit_button("🗑️ Confirm Removal", type="primary", disabled=not confirm_delete)

        if member_delete and confirm_delete:
            with st.spinner("Removing member from system..."):
                result = delete_member(selected_member_name)
            
            if "removed" in result.lower():
                st.success(f"✅ {result}")
                st.session_state.df = member_list()
                st.session_state.delete_form_member = False
                st.rerun()
            else:
                st.error(f"❌ {result}")
    
    st.markdown('</div>', unsafe_allow_html=True)