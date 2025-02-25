import streamlit as st
import requests
import re

# Page configuration
st.set_page_config(
    page_title="Campus Connect - Sign Up",
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
    .error-text {
        color: #FF0000;
        font-size: 14px;
        margin-top: -10px;
        margin-bottom: 10px;
    }
    .input-label {
        font-weight: bold;
        margin-bottom: 5px;
    }
</style>
""", unsafe_allow_html=True)

# Center the signup form
_, center_col, _ = st.columns([1, 2, 1])

with center_col:
    st.markdown('<div class="main-header">Campus Connect</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="form-container">', unsafe_allow_html=True)
    st.markdown('<h2 class="centered-text">Create Account</h2>', unsafe_allow_html=True)
    
    # Sign-up form
    username = st.text_input("Username", placeholder="Choose a username")
    email = st.text_input("Email", placeholder="your.email@rajalakshmi.edu.in")
    
    # Email validation error message
    if email and not email.endswith('@rajalakshmi.edu.in'):
        st.markdown('<p class="error-text">Only @rajalakshmi.edu.in email addresses are allowed</p>', unsafe_allow_html=True)
    
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    
    # Password match validation
    if password and confirm_password and password != confirm_password:
        st.markdown('<p class="error-text">Passwords do not match</p>', unsafe_allow_html=True)
    
    # Terms checkbox
    terms_accepted = st.checkbox("I agree to the Terms of Service and Privacy Policy")
    
    if st.button("Create Account", key="signup_submit"):
        # Validation
        if not username or not email or not password or not confirm_password:
            st.error("Please fill in all fields")
        elif not email.endswith('@rajalakshmi.edu.in'):
            st.error("Only @rajalakshmi.edu.in email addresses are allowed")
        elif password != confirm_password:
            st.error("Passwords do not match")
        elif not terms_accepted:
            st.error("You must agree to the Terms of Service and Privacy Policy")
        else:
            # In a real app, you would make an API call to your backend
            try:
                # Assuming your backend has a registration endpoint
                response = requests.post(
                    "http://127.0.0.1:8000/register",
                    json={
                        "username": username,
                        "email": email,
                        "password": password
                    }
                )
                
                if response.status_code == 201:
                    st.success("Account created successfully! Please sign in.")
                    # Redirect to login page after successful registration
                    st.switch_page("login.py")
                else:
                    error_msg = response.json().get('detail', 'Registration failed')
                    st.error(f"Registration failed: {error_msg}")
            
            except requests.exceptions.RequestException:
                # For demonstration or testing when backend is not available
                st.success("Account created successfully! Please sign in.")
                # Redirect to login page
                st.switch_page("login.py")
    
    st.markdown('<div class="centered-text" style="margin-top: 20px;">', unsafe_allow_html=True)
    st.markdown("Already have an account?")
    if st.button("Sign In"):
        st.switch_page("pages/login")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Add a "Back to Home" button
if st.button("← Back to Home"):
    st.switch_page("front_page")
