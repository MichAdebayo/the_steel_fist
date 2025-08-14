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
    
    /* Custom color variables */
    :root {
        --primary-blue: #4F46E5;
        --secondary-blue: #6366F1;
        --accent-purple: #8B5CF6;
        --success-green: #10B981;
        --warning-orange: #F59E0B;
        --error-red: #EF4444;
        --dark-gray: #1F2937;
        --light-gray: #F3F4F6;
        --white: #FFFFFF;
        --gradient-primary: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --gradient-secondary: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        --gradient-success: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    }
    
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    
    /* Main container styling */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
        font-family: 'Inter', sans-serif;
    }
    
    /* Header styling */
    .main-header {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        padding: 1rem 2rem;
        border-radius: 0 0 20px 20px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        margin-bottom: 2rem;
    }
    
    /* Card styling */
    .metric-card {
        background: rgba(255, 255, 255, 0.95);
        padding: 1.5rem;
        border-radius: 16px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        margin: 1rem 0;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
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
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(79, 70, 229, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(79, 70, 229, 0.4);
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
        border-color: var(--primary-blue);
        box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
    }
    
    .stSelectbox > div > div > select {
        border-radius: 12px;
        border: 2px solid #E5E7EB;
        padding: 0.75rem 1rem;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
    }
    
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
    
    /* Welcome card */
    .welcome-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        padding: 3rem 2rem;
        border-radius: 24px;
        text-align: center;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.1);
        margin: 2rem 0;
    }
    
    .welcome-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: var(--dark-gray);
        margin-bottom: 1rem;
    }
    
    .welcome-subtitle {
        font-size: 1.2rem;
        color: #6B7280;
        margin-bottom: 2rem;
    }
    
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
    .coach-card {
        background: white;
        padding: 1.5rem;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
        border-left: 4px solid var(--primary-blue);
    }
    
    .coach-name {
        font-size: 1.2rem;
        font-weight: 600;
        color: var(--dark-gray);
        margin-bottom: 0.5rem;
    }
    
    .coach-specialty {
        background: var(--gradient-primary);
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.875rem;
        display: inline-block;
    }
    
    /* Course card styling */
    .course-card {
        background: white;
        padding: 1.5rem;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
        position: relative;
        overflow: hidden;
    }
    
    .course-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
        background: var(--gradient-secondary);
    }
    
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
    <div class="metric-card fade-in">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <div style="font-size: 0.875rem; color: #6B7280; margin-bottom: 0.5rem;">{title}</div>
                <div style="font-size: 2rem; font-weight: 700; color: #1F2937;">{value}</div>
                {delta_html}
            </div>
            <div style="font-size: 2rem; opacity: 0.7;">{icon}</div>
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
