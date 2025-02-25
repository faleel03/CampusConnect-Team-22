import streamlit as st
import requests
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="User Profile | Campus Connect",
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
    .profile-container {
        background-color: #FFFFFF;
        border-radius: 5px;
        padding: 20px;
        margin-bottom: 15px;
        border: 1px solid #E5E5E5;
    }
    .stat-card {
        background-color: #F8F9FA;
        border-radius: 5px;
        padding: 15px;
        text-align: center;
        border: 1px solid #E5E5E5;
    }
    .stat-value {
        font-size: 24px;
        font-weight: bold;
        color: #FF4500;
    }
    .stat-label {
        font-size: 14px;
        color: #787C7E;
    }
    .post-container {
        background-color: #FFFFFF;
        border-radius: 5px;
        padding: 15px;
        margin-bottom: 15px;
        border: 1px solid #E5E5E5;
    }
    .post-title {
        font-size: 18px;
        font-weight: bold;
        color: #222222;
    }
    .community-badge {
        background-color: #0079D3;
        color: white;
        padding: 2px 8px;
        border-radius: 10px;
        font-size: 12px;
    }
    .tab-content {
        padding: 20px 0;
    }
</style>
""", unsafe_allow_html=True)

# Mock user data (in a real app, this would come from your backend)
# This would be replaced with an API call to get the user profile
def get_user_data():
    # In a real app, fetch this from the backend
    # Simulated user data
    return {
        "username": "student_dev",
        "display_name": "Campus Developer",
        "email": "dev@campus.edu",
        "join_date": "2024-12-01T00:00:00",
        "karma": 1250,
        "bio": "Computer Science major with a passion for web development and community building.",
        "communities_count": 8,
        "posts_count": 15,
        "comments_count": 42
    }

user_data = get_user_data()

# Back button
if st.button("← Back to Home"):
    st.switch_page("front_page.py")

# Profile header
st.markdown('<div class="profile-container">', unsafe_allow_html=True)

# Profile layout
col1, col2 = st.columns([1, 3])

with col1:
    # Profile avatar (placeholder)
    st.image("https://www.gravatar.com/avatar/00000000000000000000000000000000?d=mp&f=y&s=150")
    
    # Edit profile button
    if st.button("Edit Profile"):
        st.switch_page("edit_profile.py")

with col2:
    st.markdown(f"# {user_data['display_name']}")
    st.markdown(f"u/{user_data['username']}")
    
    # Join date
    join_date = datetime.fromisoformat(user_data['join_date'])
    st.markdown(f"🗓️ Joined {join_date.strftime('%B %Y')}")
    
    # Bio
    st.markdown(f"_{user_data['bio']}_")

st.markdown('</div>', unsafe_allow_html=True)

# User stats
st.markdown('<div class="profile-container">', unsafe_allow_html=True)

stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)

with stat_col1:
    st.markdown('<div class="stat-card">', unsafe_allow_html=True)
    st.markdown(f'<div class="stat-value">{user_data["karma"]}</div>', unsafe_allow_html=True)
    st.markdown('<div class="stat-label">Karma</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with stat_col2:
    st.markdown('<div class="stat-card">', unsafe_allow_html=True)
    st.markdown(f'<div class="stat-value">{user_data["posts_count"]}</div>', unsafe_allow_html=True)
    st.markdown('<div class="stat-label">Posts</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with stat_col3:
    st.markdown('<div class="stat-card">', unsafe_allow_html=True)
    st.markdown(f'<div class="stat-value">{user_data["comments_count"]}</div>', unsafe_allow_html=True)
    st.markdown('<div class="stat-label">Comments</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with stat_col4:
    st.markdown('<div class="stat-card">', unsafe_allow_html=True)
    st.markdown(f'<div class="stat-value">{user_data["communities_count"]}</div>', unsafe_allow_html=True)
    st.markdown('<div class="stat-label">Communities</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Activity tabs
tabs = st.tabs(["Posts", "Comments", "Communities", "Saved"])

# Sample post data (in a real app, this would come from your backend)
sample_posts = [
    {
        "id": "1",
        "title": "New features in Python 3.12 every student should know",
        "content": "With Python 3.12 released last month, there are several features that make coding more efficient...",
        "community_name": "cs",
        "created_at": "2025-02-20T15:30:00",
        "upvotes": 125,
        "comment_count": 18
    },
    {
        "id": "2",
        "title": "Campus hackathon announcement - $5000 in prizes!",
        "content": "Our annual hackathon will take place next month with exciting challenges and prizes...",
        "community_name": "announcements",
        "created_at": "2025-02-15T10:45:00",
        "upvotes": 89,
        "comment_count": 24
    },
    {
        "id": "3",
        "title": "Best study spots on campus? Need quiet place for finals",
        "content": "Looking for recommendations on the best places to study that are quiet and have good wifi...",
        "community_name": "campuslife",
        "created_at": "2025-02-10T09:15:00",
        "upvotes": 42,
        "comment_count": 31
    }
]

# Sample comment data
sample_comments = [
    {
        "id": "1",
        "post_title": "Any tips for freshman CS students?",
        "content": "Definitely learn Git early. Version control will save you so much headache later!",
        "community_name": "cs",
        "created_at": "2025-02-22T13:20:00",
        "upvotes": 35
    },
    {
        "id": "2",
        "post_title": "Campus WiFi down in Engineering Building?",
        "content": "It's been intermittent all week. IT said they're upgrading the routers in that area.",
        "community_name": "campuslife",
        "created_at": "2025-02-19T16:45:00",
        "upvotes": 12
    },
    {
        "id": "3",
        "post_title": "Recommended electives for Spring semester?",
        "content": "Introduction to AI (CS 440) is excellent. Professor Wilson makes complex topics accessible.",
        "community_name": "academics",
        "created_at": "2025-02-14T11:30:00",
        "upvotes": 28
    }
]

# Sample community data
sample_communities = [
    {
        "id": "1",
        "name": "cs",
        "description": "Computer Science discussions, projects, questions and resources",
        "members_count": 1250,
        "posts_count": 324
    },
    {
        "id": "2",
        "name": "campuslife",
        "description": "Everything about campus events, facilities, and student life",
        "members_count": 3540,
        "posts_count": 892
    },
    {
        "id": "3",
        "name": "hackathon",
        "description": "Organize and participate in campus hackathons and coding competitions",
        "members_count": 768,
        "posts_count": 145
    }
]

# Posts tab
with tabs[0]:
    st.markdown('<div class="tab-content">', unsafe_allow_html=True)
    
    # In a real app, fetch user posts from backend
    for post in sample_posts:
        st.markdown('<div class="post-container">', unsafe_allow_html=True)
        
        # Post header
        st.markdown(
            f'<span class="community-badge">c/{post["community_name"]}</span> '
            f'<span class="post-metadata">Posted {datetime.fromisoformat(post["created_at"]).strftime("%b %d, %Y")}</span>',
            unsafe_allow_html=True
        )
        
        # Post title
        st.markdown(f'<div class="post-title">{post["title"]}</div>', unsafe_allow_html=True)
        
        # Post content
        st.write(post["content"])
        
        # Post stats
        st.write(f"👍 {post['upvotes']} upvotes • 💬 {post['comment_count']} comments")
        
        # Action buttons
        col1, col2, col3 = st.columns(3)
        with col1:
            st.button("View Post", key=f"view_post_{post['id']}")
        with col2:
            st.button("Edit", key=f"edit_post_{post['id']}")
        with col3:
            st.button("Delete", key=f"delete_post_{post['id']}")
            
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Comments tab
with tabs[1]:
    st.markdown('<div class="tab-content">', unsafe_allow_html=True)
    
    # In a real app, fetch user comments from backend
    for comment in sample_comments:
        st.markdown('<div class="post-container">', unsafe_allow_html=True)
        
        # Comment context
        st.markdown(
            f'<span class="post-metadata">Comment on <strong>{comment["post_title"]}</strong> in '
            f'<span class="community-badge">c/{comment["community_name"]}</span> • '
            f'{datetime.fromisoformat(comment["created_at"]).strftime("%b %d, %Y")}</span>',
            unsafe_allow_html=True
        )
        
        # Comment content
        st.write(comment["content"])
        
        # Comment stats
        st.write(f"👍 {comment['upvotes']} upvotes")
        
        # Action buttons
        col1, col2, col3 = st.columns(3)
        with col1:
            st.button("View Context", key=f"view_comment_{comment['id']}")
        with col2:
            st.button("Edit", key=f"edit_comment_{comment['id']}")
        with col3:
            st.button("Delete", key=f"delete_comment_{comment['id']}")
            
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Communities tab
with tabs[2]:
    st.markdown('<div class="tab-content">', unsafe_allow_html=True)
    
    # In a real app, fetch user communities from backend
    community_cols = st.columns(3)
    
    for i, community in enumerate(sample_communities):
        with community_cols[i % 3]:
            st.markdown('<div class="post-container">', unsafe_allow_html=True)
            
            # Community name
            st.markdown(f"### c/{community['name']}")
            
            # Community description
            st.write(community["description"])
            
            # Community stats
            st.write(f"👥 {community['members_count']} members • 📝 {community['posts_count']} posts")
            
            # Action button
            st.button("Visit", key=f"visit_community_{community['id']}")
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Saved tab
with tabs[3]:
    st.markdown('<div class="tab-content">', unsafe_allow_html=True)
    
    st.info("You don't have any saved posts or comments yet.")
    
    st.markdown('</div>', unsafe_allow_html=True)
