import streamlit as st
import requests

# Page configuration
st.set_page_config(
    page_title="Create a Community | Campus Connect",
    page_icon="🎓"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 28px;
        font-weight: bold;
        color: #FF4500;
        margin-bottom: 20px;
    }
    .form-container {
        background-color: #FFFFFF;
        border-radius: 5px;
        padding: 20px;
        margin-bottom: 15px;
        border: 1px solid #E5E5E5;
    }
    .info-text {
        font-size: 14px;
        color: #787C7E;
        margin-bottom: 15px;
    }
    .styled-button {
        background-color: #FF4500;
        color: white;
        border-radius: 20px;
        padding: 5px 15px;
        border: none;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">Create a Community</div>', unsafe_allow_html=True)

# Back button
if st.button("← Back to Home"):
    st.switch_page("front_page.py")

st.markdown('<div class="form-container">', unsafe_allow_html=True)

# Community creation form
st.markdown('<div class="info-text">Communities are where users gather to discuss shared interests. Create one to start discussions on your favorite topics.</div>', unsafe_allow_html=True)

# Name field with validation
name = st.text_input("Community Name", help="Name must be between 3-21 characters, only contain letters, numbers, or underscores")
if name:
    if not (3 <= len(name) <= 21):
        st.warning("Community name must be between 3 and 21 characters.")
    if not all(c.isalnum() or c == '_' for c in name):
        st.warning("Community name can only contain letters, numbers, and underscores.")

# Description field
description = st.text_area("Description", 
                           help="Tell potential members what your community is about",
                           placeholder="Describe your community...")

# Community type
community_type = st.radio(
    "Community Type",
    ["Public", "Restricted", "Private"],
    index=0,
    help="Public: Anyone can view and post. Restricted: Anyone can view, but only approved users can post. Private: Only approved users can view and post."
)

# Visibility mapping
visibility_map = {
    "Public": "public",
    "Restricted": "restricted",
    "Private": "private"
}

# Additional settings
with st.expander("Additional Settings"):
    adult_content = st.checkbox("18+ Adult Content", help="Mark this community as NSFW (Not Safe For Work)")
    community_topics = st.multiselect(
        "Topics",
        ["Education", "Technology", "Science", "Arts", "Sports", "Entertainment", "Lifestyle", "Politics", "News", "Gaming", "Other"],
        help="Select topics that describe your community"
    )

# Form submission
user_email = st.text_input("Your Email", help="You'll be the moderator of this community")

submit_col1, submit_col2 = st.columns([3, 1])
with submit_col2:
    create_button = st.button("Create Community")

if create_button:
    if not name or not description or not user_email:
        st.error("Please fill all required fields")
    else:
        # Prepare data for API
        data = {
            "name": name,
            "description": description,
            "visibility": visibility_map.get(community_type, "public"),
            "created_by": user_email,
            "adult_content": adult_content if 'adult_content' in locals() else False,
            "topics": community_topics if 'community_topics' in locals() else []
        }
        
        try:
            # Send request to backend API
            with st.spinner("Creating your community..."):
                response = requests.post("http://127.0.0.1:8000/create_community", json=data)
                
                if response.status_code == 200:
                    result = response.json()
                    st.success(f"Community created successfully!")
                    
                    # Store new community in session state
                    if 'communities' not in st.session_state:
                        st.session_state.communities = []
                    
                    st.session_state.communities.append({
                        "id": result.get("community_id"),
                        "name": name,
                        "description": description
                    })
                    
                    # Offer to redirect
                    st.markdown("What would you like to do next?")
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("Go to your new community"):
                            st.session_state['selected_community'] = result.get("community_id")
                            st.switch_page("community_view.py")
                    with col2:
                        if st.button("Create another community"):
                            st.experimental_rerun()
                else:
                    error_message = response.json().get("detail", "Unknown error occurred")
                    st.error(f"Error: {error_message}")
        except requests.exceptions.RequestException as e:
            st.error(f"Failed to connect to backend: {e}")
            st.info("Make sure your backend server is running at http://127.0.0.1:8000")

st.markdown('</div>', unsafe_allow_html=True)

# Community Guidelines
st.markdown("""
### Community Guidelines

When creating a community, please remember:

1. **Be respectful**: Ensure your community fosters a welcoming environment
2. **Follow campus rules**: Communities must comply with institutional policies
3. **Moderate responsibly**: As a creator, you're responsible for maintaining community standards
4. **Start conversations**: The best communities are active and engaging
""")
