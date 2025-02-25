import streamlit as st
import requests
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Create a Post | Campus Connect",
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
    .tab-content {
        padding: 15px 0;
    }
    .info-text {
        font-size: 14px;
        color: #787C7E;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">Create a Post</div>', unsafe_allow_html=True)

# Back button
if st.button("← Back to Home"):
    st.switch_page("front_page.py")

st.markdown('<div class="form-container">', unsafe_allow_html=True)

# Get available communities from backend
try:
    response = requests.get("http://127.0.0.1:8000/get_communities")
    if response.status_code == 200:
        communities = response.json()
        community_names = [f"c/{comm['name']}" for comm in communities]
        
        # Use default community if coming from a specific community page
        default_idx = 0
        if 'selected_community' in st.session_state:
            for i, comm in enumerate(communities):
                if comm['id'] == st.session_state['selected_community']:
                    default_idx = i
                    break
        
        selected_community = st.selectbox(
            "Choose a community",
            community_names,
            index=default_idx
        )
        
        # Extract the community ID for the selected community
        selected_community_name = selected_community.replace("c/", "")
        selected_community_id = next((comm['id'] for comm in communities if comm['name'] == selected_community_name), None)
    else:
        st.error("Failed to fetch communities")
        communities = []
        community_names = ["No communities available"]
        selected_community = "No communities available"
        selected_community_id = None
except requests.exceptions.RequestException:
    st.error("Could not connect to backend")
    communities = []
    community_names = ["No communities available"]
    selected_community = "No communities available"
    selected_community_id = None

# Post type tabs
post_type = st.radio("Post Type", ["Text", "Image", "Link", "Poll"], horizontal=True)

# Title field (common to all post types)
post_title = st.text_input("Title", max_chars=300)

# Different form fields based on post type
if post_type == "Text":
    st.markdown('<div class="tab-content">', unsafe_allow_html=True)
    post_content = st.text_area("Text (optional)", height=200)
    st.markdown('</div>', unsafe_allow_html=True)

elif post_type == "Image":
    st.markdown('<div class="tab-content">', unsafe_allow_html=True)
    post_image = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png", "gif"])
    post_caption = st.text_area("Caption (optional)", height=100)
    st.markdown('</div>', unsafe_allow_html=True)

elif post_type == "Link":
    st.markdown('<div class="tab-content">', unsafe_allow_html=True)
    post_url = st.text_input("URL")
    post_description = st.text_area("Description (optional)", height=100)
    st.markdown('</div>', unsafe_allow_html=True)

elif post_type == "Poll":
    st.markdown('<div class="tab-content">', unsafe_allow_html=True)
    poll_description = st.text_area("Poll Description (optional)", height=100)
    
    # Dynamic poll options
    if 'poll_options' not in st.session_state:
        st.session_state.poll_options = ["", ""]
    
    # Display existing options
    for i, option in enumerate(st.session_state.poll_options):
        st.session_state.poll_options[i] = st.text_input(f"Option {i+1}", value=option, key=f"option_{i}")
    
    # Add/remove option buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Add Option") and len(st.session_state.poll_options) < 6:
            st.session_state.poll_options.append("")
            st.experimental_rerun()
    with col2:
        if st.button("Remove Last Option") and len(st.session_state.poll_options) > 2:
            st.session_state.poll_options.pop()
            st.experimental_rerun()
    
    # Poll duration
    poll_duration = st.selectbox("Poll Duration", ["1 day", "3 days", "1 week", "2 weeks"])
    st.markdown('</div>', unsafe_allow_html=True)

# Tags
post_tags = st.multiselect(
    "Tags (optional)",
    ["Question", "Announcement", "Discussion", "Help", "Advice", "Event", "Request", "Other"]
)

# Submit button
col1, col2 = st.columns([3, 1])
with col2:
    submit_post = st.button("Post")

if submit_post:
    if not post_title:
        st.error("Post title is required")
    elif selected_community_id is None:
        st.error("Please select a valid community")
    else:
        # Prepare data for API
        post_data = {
            "title": post_title,
            "community_id": selected_community_id,
            "community_name": selected_community_name,
            "post_type": post_type.lower(),
            "tags": post_tags,
            "created_at": datetime.utcnow().isoformat(),
            # In a real app, you'd get this from session/auth
            "author": st.session_state.get("username", "anonymous_user")
        }
        
        # Add post-type specific fields
        if post_type == "Text":
            post_data["content"] = post_content if 'post_content' in locals() else ""
        elif post_type == "Image":
            # In a real app, you'd handle file upload more robustly
            post_data["caption"] = post_caption if 'post_caption' in locals() else ""
            post_data["has_image"] = True if 'post_image' in locals() and post_image is not None else False
        elif post_type == "Link":
            post_data["url"] = post_url if 'post_url' in locals() else ""
            post_data["description"] = post_description if 'post_description' in locals() else ""
        elif post_type == "Poll":
            post_data["poll_description"] = poll_description if 'poll_description' in locals() else ""
            post_data["poll_options"] = st.session_state.poll_options
            post_data["poll_duration"] = poll_duration if 'poll_duration' in locals() else "1 week"
        
        # Send request to backend API
        # Note: In a real implementation, you'd need to create a corresponding endpoint in main.py
        try:
            with st.spinner("Creating your post..."):
                # This endpoint would need to be created in your backend
                response = requests.post("http://127.0.0.1:8000/create_post", json=post_data)
                
                if response.status_code == 200:
                    result = response.json()
                    st.success("Post created successfully!")
                    
                    # Offer to redirect to view the post
                    st.markdown("What would you like to do next?")
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("edit post"):
                            # Store post ID in session state
                            st.session_state['selected_post'] = result.get("post_id")
                            st.switch_page("post_view.py")
                    with col2:
                        if st.button("Go back to home"):
                            st.switch_page("front_page.py")
                else:
                    # Handle error
                    error_msg = response.json().get("detail", "Unknown error occurred")
                    st.error(f"Error: {error_msg}")
        except requests.exceptions.RequestException as e:
            st.error(f"Failed to connect to backend: {e}")
            st.info("Make sure your backend server is running at http://127.0.0.1:8000")
            
            # For development - simulate success
            st.success("Post created successfully! (Simulated)")
            
            # Offer to redirect 
            st.markdown("What would you like to do next?")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Create another post"):
                    st.experimental_rerun()
            with col2:
                if st.button("Go back to home"):
                    st.switch_page("front_page.py")

st.markdown('</div>', unsafe_allow_html=True)

# Posting guidelines
with st.expander("Posting Guidelines"):
    st.markdown("""
    ### Posting Guidelines
    
    1. **Be respectful**: Treat others with respect and kindness
    2. **Stay on topic**: Post in relevant communities
    3. **Provide context**: Clear titles and descriptions help get better engagement
    4. **Avoid duplicate posts**: Check if a similar topic already exists
    5. **Follow community rules**: Each community may have specific guidelines
    """)
