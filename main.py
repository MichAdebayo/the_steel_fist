import streamlit as st
import datetime
from styles import apply_custom_css, create_welcome_card, create_metric_card

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
        <div style="background: white; padding: 1.5rem; border-radius: 16px; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1); text-align: center; margin: 1rem 0;">
            <div style="font-size: 2rem; margin-bottom: 1rem;">👥</div>
            <h4 style="color: #1F2937; margin: 0;">Member Management</h4>
            <p style="color: #6B7280; margin: 0.5rem 0 0 0; font-size: 0.9rem;">Available</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-radius: 16px; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1); text-align: center; margin: 1rem 0;">
            <div style="font-size: 2rem; margin-bottom: 1rem;">📅</div>
            <h4 style="color: #1F2937; margin: 0;">Course Scheduling</h4>
            <p style="color: #6B7280; margin: 0.5rem 0 0 0; font-size: 0.9rem;">Active</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-radius: 16px; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1); text-align: center; margin: 1rem 0;">
            <div style="font-size: 2rem; margin-bottom: 1rem;">🏋️‍♂️</div>
            <h4 style="color: #1F2937; margin: 0;">Coach Management</h4>
            <p style="color: #6B7280; margin: 0.5rem 0 0 0; font-size: 0.9rem;">Ready</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col4:
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-radius: 16px; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1); text-align: center; margin: 1rem 0;">
            <div style="font-size: 2rem; margin-bottom: 1rem;">📊</div>
            <h4 style="color: #1F2937; margin: 0;">Analytics Dashboard</h4>
            <p style="color: #6B7280; margin: 0.5rem 0 0 0; font-size: 0.9rem;">Live</p>
        </div>
        """, unsafe_allow_html=True)

def logout():
    """Enhanced Logout Functionality"""
    st.session_state["role"] = None
    st.success("👋 Successfully logged out. See you next time!")
    st.rerun()

# Main app session state
role = st.session_state["role"]

# Navigate pages based on session state status
if st.session_state["role"] is None:
    login()
    
elif st.session_state["role"] == "Member":
    # Ensure sidebar visibility with CSS and JavaScript
    st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        display: block !important;
        visibility: visible !important;
        width: 21rem !important;
    }
    [data-testid="collapsedControl"] {
        display: block !important;
    }
    .css-1d391kg {
        width: 21rem !important;
    }
    </style>
    <script>
    // Force expand sidebar on page load
    window.addEventListener('load', function() {
        setTimeout(function() {
            const collapseBtn = parent.document.querySelector('[data-testid="collapsedControl"]');
            if (collapseBtn && getComputedStyle(collapseBtn).display !== 'none') {
                collapseBtn.click();
            }
        }, 500);
    });
    </script>
    """, unsafe_allow_html=True)
    
    # Define pages for members
    logout_page = st.Page(logout, title="🚪 Logout", icon=":material/logout:")
    settings = st.Page("pages/settings.py", title="⚙️ Settings", icon=":material/settings:")
    member_registration = st.Page("app_members.py", title="📝 Course Registration", icon="👤", default=True)
    course_register = st.Page("pages/course_registration.py", title="🎯 Browse Courses", icon="📚")
    
    # Group member pages
    account_pages = [logout_page, settings]
    member_pages = [member_registration, course_register]
    
    # Modern sidebar for members
    with st.sidebar:
        # Add a notice about sidebar visibility
        if st.button("🔄 Refresh Navigation", help="Click if navigation is not visible"):
            st.rerun()
            
        st.markdown("""
        <div style="text-align: center; padding: 1rem;">
            <h2 style="color: #4F46E5; margin-bottom: 0;">🏋️‍♂️ Steel Fist</h2>
            <p style="color: #6B7280; margin: 0;">Member Portal</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # User info
        st.markdown("""
        <div class="user-info">
            <div style="display: flex; align-items: center;">
                <div style="width: 40px; height: 40px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-right: 0.75rem;">
                    <span style="color: white; font-weight: bold;">👤</span>
                </div>
                <div>
                    <p style="margin: 0; font-weight: 600; color: #1F2937;">Member User</p>
                    <p style="margin: 0; font-size: 0.875rem; color: #6B7280;">Active Member</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Navigation for members
    pg = st.navigation(
        {
            "🏠 Member Area": member_pages,
            "⚙️ Account": account_pages,
        }
    )
    pg.run()

elif st.session_state["role"] == "Admin":
    # Ensure sidebar visibility with CSS and JavaScript
    st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        display: block !important;
        visibility: visible !important;
        width: 21rem !important;
    }
    [data-testid="collapsedControl"] {
        display: block !important;
    }
    .css-1d391kg {
        width: 21rem !important;
    }
    </style>
    <script>
    // Force expand sidebar on page load
    window.addEventListener('load', function() {
        setTimeout(function() {
            const collapseBtn = parent.document.querySelector('[data-testid="collapsedControl"]');
            if (collapseBtn && getComputedStyle(collapseBtn).display !== 'none') {
                collapseBtn.click();
            }
        }, 500);
    });
    </script>
    """, unsafe_allow_html=True)
    
    # Define pages for admins
    logout_page = st.Page(logout, title="🚪 Logout", icon=":material/logout:")
    settings = st.Page("pages/settings.py", title="⚙️ Settings", icon=":material/settings:")
    manage_coaches = st.Page("pages/manage_coaches.py", title="👨‍🏫 Manage Coaches", icon="🏋️", default=True)
    manage_courses = st.Page("pages/manage_courses.py", title="📚 Manage Courses", icon="📚")
    manage_members = st.Page("pages/manage_members.py", title="👥 Manage Members", icon="👥")
    view_registered_users = st.Page("pages/view_registered_users.py", title="📋 View Registrations", icon="📋")
    
    # Group admin pages
    account_pages = [logout_page, settings]
    admin_pages = [manage_coaches, manage_courses, manage_members, view_registered_users]
    
    # Modern sidebar for admins
    with st.sidebar:
        # Add a notice about sidebar visibility
        if st.button("🔄 Refresh Navigation", help="Click if navigation is not visible"):
            st.rerun()
            
        st.markdown("""
        <div style="text-align: center; padding: 1rem;">
            <h2 style="color: #4F46E5; margin-bottom: 0;">🏋️‍♂️ Steel Fist</h2>
            <p style="color: #6B7280; margin: 0;">Admin Dashboard</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Admin info
        st.markdown("""
        <div class="user-info">
            <div style="display: flex; align-items: center;">
                <div style="width: 40px; height: 40px; background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-right: 0.75rem;">
                    <span style="color: white; font-weight: bold;">🔑</span>
                </div>
                <div>
                    <p style="margin: 0; font-weight: 600; color: #1F2937;">Admin User</p>
                    <p style="margin: 0; font-size: 0.875rem; color: #6B7280;">System Administrator</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Quick stats
        st.markdown("### 📊 Quick Stats")
        st.markdown("""
        <div class="quick-stats">
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                <span style="color: #6B7280;">Members:</span>
                <span style="font-weight: 600; color: #10B981;">142</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                <span style="color: #6B7280;">Coaches:</span>
                <span style="font-weight: 600; color: #3B82F6;">8</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                <span style="color: #6B7280;">Active Courses:</span>
                <span style="font-weight: 600; color: #F59E0B;">24</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Navigation for admins
    pg = st.navigation(
        {
            "🛠️ Management": admin_pages,
            "⚙️ Account": account_pages,
        }
    )
    pg.run()
