import streamlit as st
import requests
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Campus Connect - Community View",
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
    }
    .community-header {
        background-color: #FFFFFF;
        border-radius: 5px;
        padding: 15px;
        margin-bottom: 15px;
        border: 1px solid #E5E5E5;
    }
    .community-title {
        font-size: 24px;
        font-weight: bold;
        color: #222222;
    }
    .community-stats {
        font-size: 14px;
        color: #787C7E;
    }
    .community-description {
        margin-top: 10px;
        font-size: 16px;
    }
    .post-container {
        background-color: #FFFFFF;
        border-radius: 5px;
        padding: 15px;
        margin-bottom: 15px;
        border: 1px solid #E5E5E5;
    }
    .post-title {
        font-size: 20px;
        font-weight: bold;
        color: #222222;
    }
    .post-metadata {
        font-size: 12px;
        color: #787C7E;
    }
    .sidebar-container {
        background-color: #FFFFFF;
        border-radius: 5px;
        padding: 15px;
        margin-bottom: 15px;
        border: 1px solid #E5E5E5;
    }
    .rule-container {
        padding: 8px 0;
        border-bottom: 1px solid #E5E5E5;
    }
    .rule-title {
        font-weight: bold;
    }
    .upvote-count {
        font-weight: bold;
        font-size: 16px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Check if community is selected, otherwise redirect
if 'selected_community' not in st.session_state:
    st.error("No community selected.")
    if st.button("Return to Home"):
        st.switch_page("front_page.py")
    st.stop()

# Get community ID from session state
community_id = st.session_state['selected_community']

# Create a two-column layout
left_column, main_column = st.columns([1, 3])

# Try to fetch community data
try:
    # In a real app, fetch from your backend
    response = requests.get(f"http://127.0.0.1:8000/get_community/{community_id}")
    if response.status_code == 200:
        community = response.json()
    else:
        st.error("Failed to load community data")
        community = None
except requests.exceptions.RequestException:
    # Sample data for demonstration
    community = {
        "id": community_id,
        "name": "Computer Science",
        "description": "A community for CS students to discuss coursework, programming, and career opportunities.",
        "member_count": 1245,
        "created_at": "2024-09-01T10:30:00",
        "created_by": "cs_admin",
        "rules": [
            {"title": "Be respectful", "description": "Treat others as you would like to be treated."},
            {"title": "No plagiarism", "description": "Do not share assignments or exam answers."},
            {"title": "Stay on topic", "description": "Keep discussions related to Computer Science."}
        ],
        "moderators": ["cs_admin", "prof_smith", "ta_jones"],
        "is_joined": True  # For demonstration
    }

# Sidebar (Left Column)
with left_column:
    # Navigation button to go back to home
    if st.button("← Back to Home"):
        st.switch_page("front_page.py")
    
    # About Community section
    st.markdown('<div class="sidebar-container">', unsafe_allow_html=True)
    st.markdown("### About Community")
    
    if community:
        st.markdown(f"**Created:** {community.get('created_at', 'Unknown')}")
        st.markdown(f"**Members:** {community.get('member_count', 0)}")
        st.markdown(f"**Founded by:** u/{community.get('created_by', 'Unknown')}")
        
        # Join/Leave button
        if community.get('is_joined', False):
            if st.button("Leave Community"):
                # API call to leave community would go here
                st.experimental_rerun()
        else:
            if st.button("Join Community"):
                # API call to join community would go here
                st.experimental_rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Community Rules
    if community and 'rules' in community:
        st.markdown('<div class="sidebar-container">', unsafe_allow_html=True)
        st.markdown("### Community Rules")
        
        for i, rule in enumerate(community['rules']):
            st.markdown(
                f"""<div class="rule-container">
                    <div class="rule-title">{i+1}. {rule['title']}</div>
                    <div>{rule['description']}</div>
                </div>""", 
                unsafe_allow_html=True
            )
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Moderators section
    if community and 'moderators' in community:
        st.markdown('<div class="sidebar-container">', unsafe_allow_html=True)
        st.markdown("### Moderators")
        
        for mod in community['moderators']:
            st.markdown(f"u/{mod}")
        
        st.markdown("</div>", unsafe_allow_html=True)

# Main Content (Right Column)
with main_column:
    # Community header
    if community:
        st.markdown('<div class="community-header">', unsafe_allow_html=True)
        st.markdown(f'<div class="community-title">c/{community.get("name", "Unknown")}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="community-stats">{community.get("member_count", 0)} members</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="community-description">{community.get("description", "")}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Create Post button
    if st.button("➕ Create Post in this Community"):
        # Store community in session state for post creation
        st.session_state['post_community'] = community_id
        st.switch_page("pages/create_post.py")
    
    # Filtering options
    st.markdown('<div class="sidebar-container">', unsafe_allow_html=True)
    filter_col1, filter_col2 = st.columns(2)
    
    with filter_col1:
        sort_by = st.selectbox("Sort By", ["Hot", "New", "Top", "Rising"])
    
    with filter_col2:
        time_filter = st.selectbox("Time", ["Today", "This Week", "This Month", "All Time"])
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Posts section
    st.markdown("### Posts")
    
    try:
        # Fetching posts for this community from the backend
        response = requests.get(f"http://127.0.0.1:8000/get_community_posts/{community_id}")
        
        if response.status_code == 200:
            posts = response.json()
            
            if not posts:
                st.info(f"No posts in this community yet! Be the first to create one.")
            
            for post in posts:
                # Post display logic (same as front_page.py)
                pass  # Replace 'pass' with actual post display logic
        
        else:  # ✅ Moved outside of the for loop, properly aligned
            st.error("Failed to fetch posts.")

    except requests.exceptions.RequestException:
        # Sample posts for demonstration
        sample_posts = [
            {
                "id": "101",
                "title": "Tips for Data Structures Final Exam",
                "content": "I'm preparing for the DS final and wanted to share some study resources I found helpful. Anyone else have recommendations?",
                "author": "cs_student123",
                "created_at": "2025-02-24T15:30:00",
                "upvotes": 32,
                "comment_count": 12
            },
            {
                "id": "102",
                "title": "Internship Opportunity at Tech Solutions",
                "content": "My company is looking for summer interns who are proficient in Python and have some experience with web development. Great opportunity for sophomores and juniors. DM me for details.",
                "author": "alumni2022",
                "created_at": "2025-02-23T09:45:00",
                "upvotes": 45,
                "comment_count": 23
            },
            {
                "id": "103",
                "title": "Project Showcase: Campus Navigation App",
                "content": "For my senior project, I built a mobile app to help students navigate our campus, find classrooms, and check building hours. Would love some feedback before my final presentation next week!",
                "author": "mobile_dev_guru",
                "created_at": "2025-02-22T14:20:00",
                "upvotes": 28,
                "comment_count": 15
            }
        ]
        
        for post in sample_posts:
            st.markdown('<div class="post-container">', unsafe_allow_html=True)
            vote_col, content_col = st.columns([1, 10])
            
            with vote_col:
                st.button("⬆️", key=f"upvote_{post['id']}")
                st.markdown(f'<div class="upvote-count">{post.get("upvotes", 0)}</div>', unsafe_allow_html=True)
                st.button("⬇️", key=f"downvote_{post['id']}")
            
            with content_col:
                st.markdown(
                    f'<span class="post-metadata">Posted by u/{post["author"]} • {post["created_at"]}</span>',
                    unsafe_allow_html=True
                )
                st.markdown(f'<div class="post-title">{post["title"]}</div>', unsafe_allow_html=True)
                st.write(post["content"])
                
                action_col1, action_col2, action_col3 = st.columns(3)
                with action_col1:
                    st.button(f"💬 {post['comment_count']} Comments", key=f"comments_{post['id']}")
                with action_col2:
                    st.button("🔄 Share", key=f"share_{post['id']}")
                with action_col3:
                    st.button("⭐ Save", key=f"save_{post['id']}")
            
            st.markdown('</div>', unsafe_allow_html=True)