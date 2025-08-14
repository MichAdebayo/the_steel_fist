import streamlit as st
import datetime
from styles import apply_custom_css, create_welcome_card, create_mmanage_members = st.Page("pages/manage_members.py", title="👥 Manage Members", icon="👥")tric_card

# Page configuration
st.set_page_config(
    page_title="Steel Fist Gym",
    page_icon="🏋️‍♂️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom styling
apply_custom_css()

# Initialize session state for role
if "role" not in st.session_state:
    st.session_state["role"] = None

ROLES = ["—", "Member", "Admin"]

def login():
    """Modern Login Page"""
    # Header with gym branding
    st.markdown("""
    <div class="main-header">
        <div style="display: flex; align-items: center; justify-content: center;">
            <h1 style="color: #4F46E5; margin: 0; font-size: 2.5rem; font-weight: 700;">
                🏋️‍♂️ Steel Fist Gym
            </h1>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Welcome section
    st.markdown(create_welcome_card(
        "Steel Fist Gym Management", 
        "Your ultimate fitness management platform. Please select your role to continue.",
        "Welcome"
    ), unsafe_allow_html=True)
    
    # Login form in the center
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown("### 🔐 Access Portal")
        st.markdown("Choose your role to access the dashboard")
        
        role = st.selectbox(
            "Select your role:",
            ROLES,
            index=0,
            help="Choose Member for gym member access or Admin for management functions"
        )
        
        if st.button("🚀 Enter Dashboard", use_container_width=True):
            if role != "—":
                st.session_state["role"] = role
                st.success(f"Welcome! Redirecting to {role} dashboard...")
                st.rerun()
            else:
                st.error("⚠️ Please select a valid role to continue.")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Features showcase
    st.markdown("---")
    st.markdown("### ✨ Platform Features")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(create_metric_card("Member Management", "👥", "👤"), unsafe_allow_html=True)
    
    with col2:
        st.markdown(create_metric_card("Course Scheduling", "📅", "🗓️"), unsafe_allow_html=True)
        
    with col3:
        st.markdown(create_metric_card("Coach Management", "🏋️‍♂️", "💪"), unsafe_allow_html=True)
        
    with col4:
        st.markdown(create_metric_card("Analytics Dashboard", "📊", "📈"), unsafe_allow_html=True)

def logout():
    """Enhanced Logout Functionality"""
    st.session_state["role"] = None
    st.success("👋 Successfully logged out. See you next time!")
    st.rerun()

# Main app session state
role = st.session_state["role"]

# Create all pages with modern design
logout_page = st.Page(logout, title="🚪 Logout", icon=":material/logout:")
settings = st.Page("pages/settings.py", title="⚙️ Settings", icon=":material/settings:")
dashboard = st.Page("test.py", title="📊 Dashboard")

# Member pages
member_registration = st.Page("app_members.py", title="📝 Course Registration", icon="👤", default=(role == "Member"))
course_register = st.Page("pages/course_registration.py", title="🎯 Browse Courses", icon="📚")

# Admin pages  
manage_coaches = st.Page("pages/manage_coaches.py", title="👨‍🏫 Manage Coaches", icon="🏋️", default=(role == "Admin"))
manage_courses = st.Page("pages/manage_courses.py", title="📚 Manage Courses", icon="📚")
manage_members = st.Page("pages/manage_members.py", title="👥 Manage Members", icon="�")
view_registered_users = st.Page("pages/view_registered_users.py", title="📋 View Registrations", icon="🗒️")

# Group pages by users
account_pages = [logout_page, settings]
member_pages = [member_registration, course_register]
admin_pages = [manage_coaches, manage_courses, manage_members, view_registered_users]

# Navigate pages based on session state status
if st.session_state["role"] is None:
    login()
    
elif st.session_state["role"] == "Member":
    # Modern sidebar for members
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 1rem;">
            <h2 style="color: #4F46E5; margin-bottom: 0;">🏋️‍♂️ Steel Fist</h2>
            <p style="color: #6B7280; margin: 0;">Member Portal</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # User info
        st.markdown(f"""
        <div class="metric-card">
            <div style="text-align: center;">
                <div style="font-size: 3rem; margin-bottom: 0.5rem;">👤</div>
                <div style="font-weight: 600; color: #1F2937;">Welcome Member!</div>
                <div style="color: #6B7280; font-size: 0.9rem;">Logged in as {st.session_state["role"]}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚪 Logout", use_container_width=True):
            logout()
    
    # Main content area
    st.markdown("""
    <div class="main-header">
        <h1 style="color: #4F46E5; margin: 0; text-align: center;">Member Dashboard</h1>
    </div>
    """, unsafe_allow_html=True)
    
    pg = st.navigation({"🏠 Main": member_pages, "⚙️ Account": account_pages})
    pg.run()

elif st.session_state["role"] == "Admin":
    # Modern sidebar for admins
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 1rem;">
            <h2 style="color: #4F46E5; margin-bottom: 0;">🏋️‍♂️ Steel Fist</h2>
            <p style="color: #6B7280; margin: 0;">Admin Portal</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Admin info  
        st.markdown(f"""
        <div class="metric-card">
            <div style="text-align: center;">
                <div style="font-size: 3rem; margin-bottom: 0.5rem;">👨‍💼</div>
                <div style="font-weight: 600; color: #1F2937;">Admin Dashboard</div>
                <div style="color: #6B7280; font-size: 0.9rem;">Full Access Control</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚪 Logout", use_container_width=True):
            logout()

    # Main content area
    st.markdown("""
    <div class="main-header">
        <h1 style="color: #4F46E5; margin: 0; text-align: center;">Admin Control Panel</h1>
    </div>
    """, unsafe_allow_html=True)
    
    pg = st.navigation({"🎛️ Management": admin_pages, "⚙️ Account": account_pages})
    pg.run()
    
