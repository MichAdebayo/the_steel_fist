import streamlit as st
from styles import apply_custom_css, create_welcome_card

# Global page config (set once) - avoids multiple calls error and ensures header visible for navigation
st.set_page_config(
    page_title="Steel Fist Gym",
    page_icon="🏋️‍♂️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize session state for role
if "role" not in st.session_state:
    st.session_state["role"] = None

ROLES = ["—", "Member", "Admin"]

# Define admin pages (initial placeholders before login)
manage_coaches = st.Page("pages/manage_coaches.py", title="Manage Coaches", icon="👨‍🏫", default=True)
manage_courses = st.Page("pages/manage_courses.py", title="Manage Courses", icon="📚")
manage_members = st.Page("pages/manage_members.py", title="Manage Members", icon="👥")
view_registered_users = st.Page("pages/view_registered_users.py", title="Registrations", icon="📋")
settings = st.Page("pages/settings.py", title="Settings", icon="⚙️") if st.session_state["role"] == "Admin" else None


def login():
    """Displays the login page and handles user role selection.

    This function presents the login interface, allowing users to select their role and enter the system. It configures the page, applies custom styling, and showcases platform features.

    Returns:
        None
    """
    # Apply custom styling
    apply_custom_css()
    # Ensure any previous sidebar content is cleared for a clean login view
    st.sidebar.empty()
    # Hide header (hamburger + toolbar) AND completely hide sidebar container on landing (pre-login)
    # Sidebar sometimes persists from previous session unless explicitly hidden; we target its testid.
    st.markdown("""
    <style>
    header {visibility:hidden;}
    section[data-testid="stSidebar"] {display:none !important;}
    div[data-testid="stSidebarNav"] {display:none !important;}
    </style>
    """, unsafe_allow_html=True)
    
    # Header with gym branding
    st.markdown("""
    <div class="main-header">
        <div style="display: flex; align-items: center; justify-content: center;">
            <h1 style="color: var(--brand-primary); margin: 0; font-size: 2.5rem; font-weight: 700;">
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
        st.markdown('<div class="form-container">', unsafe_allow_html=True)
        
        with st.form("login_form"):
            st.markdown("#### 🔐 Select Your Role")
            role = st.selectbox("Choose role:", ROLES[1:], index=0)
            
            if st.form_submit_button("🚀 Enter System", use_container_width=True, type="primary"):
                st.session_state["role"] = role
                st.success(f"🎉 Welcome, {role}!")
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Feature showcase
    st.markdown("---")
    st.markdown("### 🌟 Platform Features")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">👥</div>
            <h4>Member Management</h4>
            <p>Available</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📅</div>
            <h4>Course Scheduling</h4>
            <p>Active</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🏋️‍♂️</div>
            <h4>Coach Management</h4>
            <p>Ready</p>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📊</div>
            <h4>Analytics Dashboard</h4>
            <p>Live</p>
        </div>
        """, unsafe_allow_html=True)

def handle_logout():
    """Handles user logout and clears session state.

    This function displays a logout button and, when clicked, clears all session state and reruns the app to return to the login page.

    Returns:
        None
    """
    if st.button("🚪 Logout", use_container_width=True):
        # Clear all session state
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.session_state["role"] = None
        st.cache_data.clear()
        st.rerun()

def logout():
    """This should not be called directly anymore"""
    pass

# Main app logic
if st.session_state["role"] is None:
    login()
else:
    # Expand sidebar after login
    st.sidebar.empty()
    # Apply custom styling
    apply_custom_css()
    
    if st.session_state["role"] == "Admin":
        # Define admin pages (fixed invalid emojis)
        manage_coaches = st.Page("pages/manage_coaches.py", title="Manage Coaches", icon="👨‍🏫", default=True)
        manage_courses = st.Page("pages/manage_courses.py", title="Manage Courses", icon="📚")
        manage_members = st.Page("pages/manage_members.py", title="Manage Members", icon="👥")
        view_registered_users = st.Page("pages/view_registered_users.py", title="Registrations", icon="📋")
        settings = st.Page("pages/settings.py", title="Settings", icon="⚙️")
        
        # Create navigation
        pg = st.navigation({
            "Management": [manage_coaches, manage_courses, manage_members, view_registered_users],
            "Account": [settings]
        })
        
        # Custom sidebar content
        with st.sidebar:
            st.markdown("""
            <div class="brand-block">
                <h2>🏋️‍♂️ Steel Fist</h2>
                <p>Admin Dashboard</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Admin info
            st.markdown("""
            <div class="user-info">
                <div class="avatar gradient-admin">🔑</div>
                <div class="user-meta">
                    <p class="name">Admin User</p>
                    <p class="role">System Administrator</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Quick stats
            st.markdown("### 📊 Quick Stats")
            st.markdown("""
            <div class="quick-stats">
                <div class="row"><span>Members:</span><span class="value success">142</span></div>
                <div class="row"><span>Coaches:</span><span class="value info">8</span></div>
                <div class="row"><span>Active Courses:</span><span class="value warn">24</span></div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Add logout button in sidebar
            handle_logout()
        
        # Run the navigation
        pg.run()
        
    elif st.session_state["role"] == "Member":
        # Define member pages (fixed invalid emojis)
        member_registration = st.Page("app_members.py", title="Course Registration", icon="👤", default=True)
        course_register = st.Page("pages/course_registration.py", title="Browse Courses", icon="🎯")
        settings = st.Page("pages/settings.py", title="Settings", icon="⚙️")
        
        # Create navigation
        pg = st.navigation({
            "Member Area": [member_registration, course_register],
            "Account": [settings]
        })
        
        # Custom sidebar content
        with st.sidebar:
            st.markdown("""
            <div class="brand-block">
                <h2>🏋️‍♂️ Steel Fist</h2>
                <p>Member Portal</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # User info
            st.markdown("""
            <div class="user-info">
                <div class="avatar gradient-member">👤</div>
                <div class="user-meta">
                    <p class="name">Member User</p>
                    <p class="role">Active Member</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Add logout button in sidebar
            handle_logout()
        
        # Run the navigation
        pg.run()
