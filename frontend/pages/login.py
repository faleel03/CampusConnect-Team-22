import streamlit as st
import requests
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Campus Connect - Login",
    page_icon="🎓",
    layout="wide"
)

# Custom CSS 
st.markdown("""
<style>
    .main-header {
        font-size: 28px;
        font-weight: bold;
        color: #FF4500;
        margin-bottom: 20px;
        text-align: center;
    }
    .form-container {
        background-color: #FFFFFF;
        border-radius: 5px;
        padding: 25px;
        margin: 0 auto;
        max-width: 500px;
        border: 1px solid #E5E5E5;
    }
    .centered-text {
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Center the login form
_, center_col, _ = st.columns([1, 2, 1])

with center_col:
    st.markdown('<div class="main-header">Campus Connect</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="form-container">', unsafe_allow_html=True)
    st.markdown('<h2 class="centered-text">Sign In</h2>', unsafe_allow_html=True)
    
    # Login form
    email = st.text_input("Email", placeholder="your.email@rajalakshmi.edu.in")
    password = st.text_input("Password", type="password")
    
    if st.button("Sign In", key="signin_submit"):
        if not email or not password:
            st.error("Please fill in all fields")
        else:
            try:
                response = requests.post(
                    "http://127.0.0.1:8000/login",
                    json={"email": email, "password": password}
                )
                
                if response.status_code == 200:
                    user_data = response.json()
                    st.session_state['logged_in'] = True
                    st.session_state['username'] = user_data.get('username', email.split('@')[0])
                    st.session_state['user_id'] = user_data.get('user_id')
                    
                    st.success("Login successful!")
                    st.switch_page("front_page")  # Redirect to front page
                else:
                    error_msg = response.json().get('detail', 'Invalid credentials')
                    st.error(f"Login failed: {error_msg}")
            
            except requests.exceptions.RequestException:
                st.error("Login failed: Unable to connect to the backend")
    
    st.markdown('<div class="centered-text" style="margin-top: 20px;">', unsafe_allow_html=True)
    st.markdown("Don't have an account?")
    if st.button("Create Account"):
        st.switch_page("pages/signup")  # Redirect to signup page
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Add a "Back to Home" button
if st.button("← Back to Home"):
    st.switch_page("front_page")
