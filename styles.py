"""
Modern styling system for The Steel Fist Gym Management App
Inspired by modern fitness applications with professional design
"""

import streamlit as st

def apply_custom_css():
    """Apply custom CSS styling to create a modern, professional look"""
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    .main {
        padding: 0;
    }
    
    /* Custom color variables (refined brand palette) */
    :root {
        /* Brand + functional colors */
    --brand-primary: hsl(350,98%,64%); /* updated brand tone */
    --brand-primary-rgb: 253,73,103; /* hsl(350,98%,64%) -> approx rgb */
        --brand-secondary: #2B2D42; /* dark slate */
        --brand-accent: #8D99AE; /* muted accent */
        --brand-accent-bright: #4FC3F7; /* bright accent for highlights */
        --bg-dark: #10141B; /* app background */
        --bg-dark-alt: #1B222C;
        --surface-elevated: #FFFFFF;
        --surface-muted: #F5F7FA;
        --text-high: #0F172A;
        --text-medium: #475569;
        --text-low: #64748B;
        --success: #16A34A;
        --warning: #F59E0B;
        --error: #DC2626;
        --info: #2563EB;
    --gradient-primary: linear-gradient(135deg, hsl(350,98%,64%) 0%, hsl(350,88%,54%) 100%);
        --gradient-secondary: linear-gradient(135deg, #2B2D42 0%, #3B4254 100%);
        --gradient-success: linear-gradient(135deg, #16A34A 0%, #10B981 100%);
        --glow-shadow: 0 8px 32px rgba(var(--brand-primary-rgb),0.35);
        --radius-sm: 8px; 
        --radius-md: 14px;
        --radius-lg: 22px;
        --focus-ring: 0 0 0 3px rgba(var(--brand-primary-rgb),0.35);
    }
    
    /* Hide some default elements (keep header for navigation) */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    /* header kept visible to allow Streamlit navigation components */
    .stDeployButton {display:none;}
    
    /* Main container styling - Dark Theme */
    .stApp {
        background: radial-gradient(circle at 30% 20%, #18202A 0%, var(--bg-dark) 60%);
        min-height: 100vh;
        font-family: 'Inter', sans-serif;
        color: #F1F5F9;
    }
    
    /* Header styling - Dark Theme */
    .main-header {
        background: linear-gradient(120deg, rgba(var(--brand-primary-rgb),0.12), rgba(255,255,255,0.04));
        backdrop-filter: blur(18px) saturate(140%);
        padding: 1rem 2rem;
        border-radius: 0 0 var(--radius-lg) var(--radius-lg);
        box-shadow: var(--glow-shadow);
        margin-bottom: 2rem;
        border: 1px solid rgba(255,255,255,0.08);
    }
    
    /* Card styling - Dark Theme */
    .metric-card {
        background: linear-gradient(160deg, #FFFFFF 0%, #F8FAFC 100%);
        padding: 1.25rem 1.35rem 1.1rem;
        border-radius: var(--radius-md);
        box-shadow: 0 4px 18px rgba(0,0,0,0.08);
        border: 1px solid #E2E8F0;
        margin: 1rem 0;
        transition: transform 0.25s ease, box-shadow 0.25s ease;
        color: var(--text-high);
    }
    
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 10px 28px rgba(0,0,0,0.12);
    }
    
    /* Stats card specific styling */
    .stats-card {
        background: var(--gradient-primary);
        color: white;
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 8px 32px rgba(79, 70, 229, 0.3);
    }
    
    .stats-number {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .stats-label {
        font-size: 1rem;
        opacity: 0.9;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Button styling */
    .stButton > button {
        background: var(--gradient-primary);
        color: #ffffff;
        border: none;
        border-radius: var(--radius-sm);
        padding: 0.65rem 1.4rem;
        font-weight: 600;
        font-size: 0.95rem;
        letter-spacing: .3px;
        transition: all 0.25s ease;
        box-shadow: 0 4px 14px rgba(var(--brand-primary-rgb),0.35);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 22px rgba(var(--brand-primary-rgb),0.45);
        filter: brightness(1.02);
        background: var(--brand-primary) !important;
        background-image: none !important;
    }
    /* Extra specificity to guarantee hover color across dynamic injections */
    .stButton > button:active, .stButton > button:focus, .stButton > button:focus-visible {
        background: var(--brand-primary) !important;
        background-image: none !important;
    }
    
    /* Form styling */
    .stTextInput > div > div > input {
        border-radius: 12px;
        border: 2px solid #E5E7EB;
        padding: 0.75rem 1rem;
        font-size: 1rem;
        transition: border-color 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: var(--brand-primary);
        box-shadow: var(--focus-ring);
    }
    
    .stSelectbox > div > div > select {
        border-radius: 12px;
        border: 2px solid #E5E7EB;
        padding: 0.75rem 1rem;
    }
    
    /* Sidebar styling - Dark Theme */
    .css-1d391kg {
        background: rgba(45, 45, 45, 0.95);
        backdrop-filter: blur(10px);
        color: #ffffff;
    }
    
    /* Update sidebar text colors */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, var(--bg-dark-alt) 0%, #12161D 100%);
        color: #E2E8F0;
        border-right: 1px solid rgba(255,255,255,0.05);
    }
    
    [data-testid="stSidebar"] * { color: #F1F5F9 !important; }

    /* Feature card styling */
    .feature-card {
        background: linear-gradient(145deg,#FFFFFF 0%,#F1F5F9 100%);
        padding: 1.2rem 1rem;
        border-radius: var(--radius-md);
        box-shadow: 0 6px 18px rgba(0,0,0,0.08);
        text-align: center;
        border: 1px solid #E2E8F0;
        transition: all .28s ease;
    }
    .feature-card h4 { margin: 0; color: var(--text-high); font-size: 1.05rem; }
    .feature-card p { margin: .45rem 0 0 0; font-size: .78rem; text-transform: uppercase; letter-spacing: .5px; color: var(--text-low); font-weight:600; }
    .feature-icon { font-size: 1.9rem; margin-bottom: .4rem; filter: drop-shadow(0 4px 6px rgba(0,0,0,0.15)); }
    .feature-card:hover { transform: translateY(-4px); box-shadow: 0 10px 26px rgba(0,0,0,0.14);}    

    /* Utility avatar and user info */
    .user-info { display:flex; align-items:center; gap:.9rem; }
    .avatar { width:52px; height:52px; display:flex; align-items:center; justify-content:center; font-size:1.5rem; font-weight:600; border-radius:18px; }
    .gradient-admin { background: var(--gradient-primary); color:#fff; box-shadow:0 4px 14px rgba(var(--brand-primary-rgb),0.4);}    
    .gradient-member { background: linear-gradient(135deg,#6366F1 0%,#4F46E5 100%); color:#fff; box-shadow:0 4px 14px rgba(99,102,241,.45);}    
    .user-meta .name { margin:0; font-weight:600; color:#fff; }
    .user-meta .role { margin:0; font-size:.75rem; letter-spacing:.5px; text-transform:uppercase; color:#94A3B8; }

    /* Quick stats rows */
    .quick-stats { font-size:.82rem; }
    .quick-stats .row { display:flex; justify-content:space-between; margin-bottom:.45rem; color:#CBD5E1; }
    .quick-stats .value { font-weight:600; }
    .quick-stats .value.success { color: var(--success); }
    .quick-stats .value.info { color: var(--info); }
    .quick-stats .value.warn { color: var(--warning); }

    .brand-block h2 { color:#fff; margin:0 0 .25rem 0; font-size:1.35rem; letter-spacing:.5px; }
    .brand-block p { margin:0; color:#94A3B8; font-size:.8rem; letter-spacing:.75px; text-transform:uppercase; }
    
    /* Table styling */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    }
    
    /* Title styling */
    .main-title {
        font-size: 3rem;
        font-weight: 700;
        color: white;
        text-align: center;
        margin: 2rem 0;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
    }
    
    .section-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: var(--dark-gray);
        margin: 1.5rem 0 1rem 0;
        border-left: 4px solid var(--primary-blue);
        padding-left: 1rem;
    }
    
    /* Welcome card - Dark Theme */
    .welcome-card {
        background: linear-gradient(135deg, rgba(var(--brand-primary-rgb),0.12) 0%, rgba(255,255,255,0.04) 100%);
        backdrop-filter: blur(24px) saturate(160%);
        padding: 2.6rem 2rem 2.3rem;
        border-radius: var(--radius-lg);
        text-align: center;
        box-shadow: var(--glow-shadow);
        margin: 2rem 0;
        color: #F8FAFC;
        border: 1px solid rgba(255,255,255,0.08);
    }
    
    .welcome-title { font-size:2.3rem; font-weight:700; color:#FFFFFF; margin-bottom:.85rem; letter-spacing:.5px; }
    
    .welcome-subtitle { font-size:1.05rem; color:#E2E8F0; margin-bottom:1.65rem; }
    
    /* Progress bar styling */
    .stProgress > div > div > div > div {
        background: var(--gradient-primary);
        border-radius: 10px;
    }
    
    /* Navigation styling */
    .nav-item {
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 12px;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .nav-item:hover {
        background: rgba(79, 70, 229, 0.1);
        transform: translateX(5px);
    }
    
    /* Coach card styling */
    .coach-card { background:#FFFFFF; padding:1.35rem 1.25rem; border-radius: var(--radius-md); box-shadow:0 4px 18px rgba(0,0,0,0.08); margin:1rem 0; border-left:4px solid var(--brand-primary); }
    
    .coach-name { font-size:1.15rem; font-weight:600; color:var(--text-high); margin-bottom:.4rem; }
    
    .coach-specialty { background: var(--gradient-primary); color:#fff; padding:0.22rem .65rem; border-radius:18px; font-size:.75rem; display:inline-block; letter-spacing:.5px; }
    
    /* Course card styling */
    .course-card { background:#FFFFFF; padding:1.4rem 1.3rem; border-radius: var(--radius-md); box-shadow:0 4px 18px rgba(0,0,0,0.08); margin:1rem 0; position:relative; overflow:hidden; }
    
    .course-card::before { content:''; position:absolute; top:0; left:0; width:5px; height:100%; background:var(--gradient-primary); }
    
    /* Status badges */
    .status-badge {
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.875rem;
        font-weight: 500;
        display: inline-block;
    }
    
    .status-active {
        background: rgba(16, 185, 129, 0.1);
        color: var(--success-green);
    }
    
    .status-full {
        background: rgba(239, 68, 68, 0.1);
        color: var(--error-red);
    }
    
    .status-available {
        background: rgba(245, 158, 11, 0.1);
        color: var(--warning-orange);
    }
    
    /* Animation classes */
    .fade-in {
        animation: fadeIn 0.5s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .slide-in-left {
        animation: slideInLeft 0.5s ease-out;
    }
    
    @keyframes slideInLeft {
        from { transform: translateX(-100px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    /* Mobile responsiveness */
    @media (max-width: 768px) {
        .main-title {
            font-size: 2rem;
        }
        
        .welcome-title {
            font-size: 1.8rem;
        }
        
        .stats-number {
            font-size: 2rem;
        }
        
        .metric-card {
            padding: 1rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)

def create_metric_card(title, value, icon="📊", delta=None, delta_color="normal"):
    """Create a modern metric card with optional delta"""
    delta_html = ""
    if delta:
        delta_color_class = "success" if delta_color == "normal" else "error"
        delta_html = f'<div class="metric-delta {delta_color_class}">▲ {delta}</div>'
    
    return f"""
    <div class=\"metric-card fade-in\">
        <div style=\"display:flex; justify-content:space-between; align-items:center;\">
            <div>
                <div style=\"font-size:.72rem; letter-spacing:.8px; font-weight:600; text-transform:uppercase; color:var(--text-low); margin-bottom:.45rem;\">{title}</div>
                <div style=\"font-size:1.85rem; font-weight:700; color:var(--text-high); line-height:1;\">{value}</div>
                {delta_html}
            </div>
            <div style=\"font-size:2rem; opacity:.6; filter:drop-shadow(0 4px 6px rgba(0,0,0,.15));\">{icon}</div>
        </div>
    </div>
    """

def create_stats_card(number, label, color="primary"):
    """Create a colorful stats card"""
    gradient_class = f"gradient-{color}"
    return f"""
    <div class="stats-card fade-in">
        <div class="stats-number">{number}</div>
        <div class="stats-label">{label}</div>
    </div>
    """

def create_welcome_card(title, subtitle, user_role="User"):
    """Create a welcome card for the dashboard"""
    return f"""
    <div class="welcome-card slide-in-left">
        <div class="welcome-title">Welcome back! 👋</div>
        <div class="welcome-subtitle">{subtitle}</div>
        <div style="background: var(--gradient-primary); color: white; padding: 0.5rem 1.5rem; border-radius: 25px; display: inline-block; font-weight: 600;">
            {user_role} Dashboard
        </div>
    </div>
    """

def create_section_header(title, icon="", description=""):
    """Create a section header with icon and description"""
    return f"""
    <div style="margin: 2rem 0 1rem 0;">
        <div class="section-title">{icon} {title}</div>
        {f'<div style="color: #6B7280; margin-left: 1rem; font-size: 0.9rem;">{description}</div>' if description else ''}
    </div>
    """

def create_action_button(text, icon="", key="", type="primary"):
    """Create a styled action button"""
    button_class = f"action-btn-{type}"
    return f"""
    <div class="{button_class}" style="
        background: var(--gradient-primary);
        color: white;
        padding: 0.75rem 1.5rem;
        border-radius: 12px;
        text-align: center;
        cursor: pointer;
        font-weight: 600;
        margin: 0.5rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(79, 70, 229, 0.3);
    ">
        {icon} {text}
    </div>
    """
