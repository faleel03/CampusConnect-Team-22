import streamlit as st
import requests
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Campus Connect",
    page_icon="🎓",
    layout="wide"
)

# Custom CSS to make it look more like Reddit
st.markdown("""
<style>
    .main-header {
        font-size: 28px;
        font-weight: bold;
        color: #FF4500;
        margin-bottom: 20px;
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
    .action-button {
        width: 100%;
        margin-bottom: 10px;
    }
    .community-badge {
        background-color: #0079D3;
        color: white;
        padding: 2px 8px;
        border-radius: 10px;
        font-size: 12px;
        margin-right: 5px;
    }
    .upvote-count {
        font-weight: bold;
        font-size: 16px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Create a two-column layout
left_column, main_column = st.columns([1, 3])

# Sidebar (Left Column)
with left_column:
    st.markdown('<div class="sidebar-container">', unsafe_allow_html=True)
    st.markdown('<div class="main-header">Campus Connect</div>', unsafe_allow_html=True)
    
    # User info section (placeholder)
    if st.session_state.get('logged_in', False):
        st.write(f"👤 Welcome, {st.session_state.get('username', 'User')}")
# Change these lines in front_page.py
    else:
        if st.button("Sign In", key="signin"):
            st.switch_page("pages/login.py")  # Updated path
        if st.button("Sign Up", key="signup"):
            st.switch_page("pages/signup.py")  # Updated path
    
    st.markdown("---")
    
    # Main action buttons
    if st.button("➕ Create Post", key="create_post_btn"):
        st.switch_page("pages/create_post.py")  # Redirect to post creation page
    
    if st.button("🌐 Create Community", key="create_community_btn"):
        st.switch_page("pages/community_creation.py")  # Redirect to community creation page
    
    st.markdown("---")
    
    # My Communities section
    st.subheader("My Communities")
    try:
        response = requests.get("http://127.0.0.1:8000/get_communities")
        if response.status_code == 200:
            communities = response.json()[:5]  # Just showing first 5 for demo
            
            for community in communities:
                community_id = community.get("id", None)  # Safely get ID
                community_name = community.get("name", "Unknown")

                if community_id is None:
                    st.warning(f"Skipping community '{community_name}' due to missing ID.")
                    continue  # Skip this iteration if ID is missing

                if st.button(f"c/{community_name}", key=f"community_{community_id}"):
                    # Store selected community in session state
                    st.session_state['selected_community'] = community_id
                    st.switch_page("community_view.py")  # Redirect to community view
        else:
            st.error("Failed to load communities")
    except requests.exceptions.RequestException:
        st.write("No communities to display")

    if st.button("See All Communities", key="see_all_communities"):
        st.switch_page("all_communities.py")  # Redirect to all communities page
    
    st.markdown("</div>", unsafe_allow_html=True)

# Main Content (Right Column)
with main_column:
    # Filtering options
    st.markdown('<div class="sidebar-container">', unsafe_allow_html=True)
    filter_col1, filter_col2, filter_col3 = st.columns(3)
    
    with filter_col1:
        sort_by = st.selectbox("Sort By", ["Hot", "New", "Top", "Rising"])
    
    with filter_col2:
        time_filter = st.selectbox("Time", ["Today", "This Week", "This Month", "All Time"])
    
    with filter_col3:
        community_filter = st.selectbox("Community", ["All Communities", "My Communities"])
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Posts section
    st.markdown("### Posts")
    
    try:
        # Fetching posts from the backend
        response = requests.get("http://127.0.0.1:8000/get_posts")
        
        if response.status_code == 200:
            posts = response.json()
            
            if not posts:
                st.info("No posts yet! Be the first to create one.")
            
            for post in posts:
                # Post container
                st.markdown('<div class="post-container">', unsafe_allow_html=True)
                
                # Post layout with upvote column and content column
                vote_col, content_col = st.columns([1, 10])
                
                with vote_col:
                    
                    post_id = str(post.get('id', ''))  # Ensure it's a string
                    user_id = str(st.session_state.get('user_id', ''))  # Ensure it's a string

                    if not post_id or not user_id:
                        st.warning("Log  in to  vote")
                    else:
                        # Upvote Button
                        if st.button("⬆️", key=f"upvote_{post_id}"):
                            try:
                                response = requests.post(
                                    "http://127.0.0.1:8000/vote",
                                    json={"post_id": post_id, "user_id": user_id, "vote_type": "upvote"}
                                )
                                st.write(response.json())  # Debugging - Show API response
                                if response.status_code == 200:
                                    st.experimental_rerun()
                                else:
                                    st.error(f"Failed to upvote: {response.text}")  # Show error message
                            except requests.exceptions.RequestException as e:
                                st.error(f"Error connecting to the server: {e}")

                        # Display Upvote Count
                        st.markdown(f'<div class="upvote-count">{post.get("upvotes", 0)}</div>', unsafe_allow_html=True)

                        # Downvote Button
                        if st.button("⬇️", key=f"downvote_{post_id}"):
                            try:
                                response = requests.post(
                                    "http://127.0.0.1:8000/vote",
                                    json={"post_id": post_id, "user_id": user_id, "vote_type": "downvote"}
                                )
                                st.write(response.json())  # Debugging - Show API response
                                if response.status_code == 200:
                                    st.experimental_rerun()
                                else:
                                    st.error(f"Failed to downvote: {response.text}")  # Show error message
                            except requests.exceptions.RequestException as e:
                                st.error(f"Error connecting to the server: {e}")

                with content_col:
                    # Community badge and post metadata
                    st.markdown(
                        f'<span class="community-badge">c/{post.get("community_name", "unknown")}</span> '
                        f'<span class="post-metadata">Posted by u/{post.get("author", "anonymous")} • '
                        f'{post.get("created_at", datetime.now().isoformat())}</span>',
                        unsafe_allow_html=True
                    )
                    
                    # Post title with link
                    st.markdown(f'<div class="post-title">{post.get("title", "Untitled Post")}</div>', unsafe_allow_html=True)
                    
                    # Post content - truncated if too long
                    content = post.get("content", "")
                    if content is None:
                        content = ""
                    if len(content) > 300:
                        content = content[:300] + "..."
                    st.write(content)
                    
                    # Post actions
                    action_col1, action_col2, action_col3 = st.columns(3)
                    with action_col1:
                        st.button(f"💬 {post.get('comment_count', 0)} Comments", key=f"comments_{post.get('id', 'unknown')}")
                    with action_col2:
                        st.button("🔄 Share", key=f"share_{post.get('id', 'unknown')}")
                    with action_col3:
                        st.button("⭐ Save", key=f"save_{post.get('id', 'unknown')}")
                
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.error("Failed to fetch posts.")
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching posts: {e}")
        
        # Display sample posts if real data can't be loaded
        sample_posts = [
            {
                "id": "1",
                "title": "Welcome to Campus Connect!",
                "content": "This is a community for students to connect and collaborate. Share your ideas, ask questions, and join the discussion!",
                "author": "admin",
                "community_name": "announcements",
                "created_at": "2025-02-22T10:30:00",
                "upvotes": 42,
                "comment_count": 15
            },
            {
                "id": "2", 
                "title": "Computer Science Study Group",
                "content": "Looking for people to join our CS study group. We meet every Tuesday at the library. All levels welcome!",
                "author": "csprogrammer",
                "community_name": "cs",
                "created_at": "2025-02-23T14:15:00",
                "upvotes": 28,
                "comment_count": 7
            }
        ]
        
        for post in sample_posts:
            st.markdown('<div class="post-container">', unsafe_allow_html=True)
            vote_col, content_col = st.columns([1, 10])
            
            with vote_col:
                st.button("⬆️", key=f"upvote_{post['id']}")
                st.markdown(f'<div class="upvote-count">{post["upvotes"]}</div>', unsafe_allow_html=True)
                st.button("⬇️", key=f"downvote_{post['id']}")
            
            with content_col:
                st.markdown(
                    f'<span class="community-badge">c/{post["community_name"]}</span> '
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
