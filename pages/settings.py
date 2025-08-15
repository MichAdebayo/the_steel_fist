# Modern Settings Page
import streamlit as st
from styles import apply_custom_css, create_welcome_card, create_section_header

# Apply modern styling
apply_custom_css()

# Page header
st.markdown(create_welcome_card(
    "System Settings", 
    "Configure your gym management system preferences and account settings",
    "Settings"
), unsafe_allow_html=True)

# Current user info
role = st.session_state.get("role", "Unknown")
st.markdown(create_section_header("👤 Account Information", "🔧", f"Currently logged in as: {role}"), unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown("### 🎨 Theme Settings")
    theme_mode = st.selectbox("Color Theme", ["Light", "Dark", "Auto"])
    language = st.selectbox("Language", ["English", "French", "Spanish"])
    notifications = st.toggle("Enable Notifications", value=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown("### 🔐 Security Settings")
    auto_logout = st.selectbox("Auto Logout", ["15 minutes", "30 minutes", "1 hour", "Never"])
    two_factor = st.toggle("Two-Factor Authentication", value=False)
    session_timeout = st.toggle("Session Timeout Warning", value=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Save button
st.markdown("---")
col1, col2, col3 = st.columns([2, 1, 2])
with col2:
    if st.button("💾 Save Settings", use_container_width=True, type="primary"):
        st.success("✅ Settings saved successfully!")
        st.balloons()