from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from datetime import datetime
import uuid
import firebase_admin
from firebase_admin import credentials, firestore
from typing import List, Optional
import hashlib

# Replace 'your-firebase-credentials.json' with your downloaded JSON key file
cred = credentials.Certificate(r"C:\Users\Faleel Mohsin\Documents\claude\backend\serviceAccountKey.json")
firebase_admin.initialize_app(cred)

# Firestore client
db = firestore.client()

app = FastAPI()

# Define User Schema
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

# Define Community Schema
class Community(BaseModel):
    name: str
    description: str
    created_by: str  # Email of the creator
    visibility: str  # "public", "restricted", or "private"
    adult_content: Optional[bool] = False
    topics: Optional[List[str]] = []

# Define Post Schema
class Post(BaseModel):
    title: str
    community_id: str
    community_name: str
    post_type: str  # "text", "image", "link", or "poll"
    author: str
    content: Optional[str] = None
    url: Optional[str] = None
    description: Optional[str] = None
    caption: Optional[str] = None
    has_image: Optional[bool] = False
    poll_description: Optional[str] = None
    poll_options: Optional[List[str]] = None
    poll_duration: Optional[str] = None
    tags: Optional[List[str]] = []

# Define Comment Schema
class Comment(BaseModel):
    post_id: str
    author: str
    content: str
    parent_id: Optional[str] = None  # For nested comments

# Define Vote Schema
class Vote(BaseModel):
    post_id: str
    user_id: str
    vote_type: str  # "upvote" or "downvote"

# Hash password function
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

@app.post("/register", status_code=201)
def register_user(user: UserCreate):
    try:
        # Check if email ends with @rajalakshmi.edu.in
        if not user.email.endswith('@rajalakshmi.edu.in'):
            raise HTTPException(status_code=400, detail="Only @rajalakshmi.edu.in email addresses are allowed")
        
        # Check if email already exists
        existing_user_email = db.collection("users").where("email", "==", user.email).get()
        if existing_user_email:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Check if username already exists
        existing_user_username = db.collection("users").where("username", "==", user.username).get()
        if existing_user_username:
            raise HTTPException(status_code=400, detail="Username already taken")
        
        # Generate unique User ID
        user_id = str(uuid.uuid4())
        user_ref = db.collection("users").document(user_id)
        
        # Hash the password
        hashed_password = hash_password(user.password)
        
        # Store user in Firestore
        user_ref.set({
            "id": user_id,
            "username": user.username,
            "email": user.email,
            "password": hashed_password,  # Store hashed password
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
            "profile_picture": None,
            "bio": None,
            "joined_communities": []
        })
        
        return {"message": "User registered successfully", "user_id": user_id}
    
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Login endpoint
class LoginRequest(BaseModel):
    email: str
    password: str

# Hashing function placeholder (implement proper hashing in production)
def hash_password(password: str) -> str:
    return password  # Replace with real hash function

# ✅ Fixed Login Endpoint
@app.post("/login")
def login_user(request: LoginRequest):
    try:
        # Get user by email
        user_query = db.collection("users").where("email", "==", request.email).limit(1).get()
        
        if not user_query:
            raise HTTPException(status_code=401, detail="Invalid email or password")
        
        user_data = user_query[0].to_dict()
        
        # Check password
        hashed_password = hash_password(request.password)
        if user_data.get("password") != hashed_password:
            raise HTTPException(status_code=401, detail="Invalid email or password")
        
        # Return user info (excluding password)
        user_info = {k: v for k, v in user_data.items() if k != "password"}
        return user_info
    
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/create_community")
def create_community(community: Community):
    try:
        # Generate unique Community ID
        community_id = str(uuid.uuid4())
        community_ref = db.collection("communities").document(community_id)

        # Check if the community name already exists
        existing_communities = db.collection("communities").where("name", "==", community.name).get()
        if existing_communities:
            raise HTTPException(status_code=400, detail="Community name already exists")

        # Store community details in Firestore
        community_ref.set({
            "id": community_id,
            "name": community.name,
            "description": community.description,
            "created_by": community.created_by,
            "visibility": community.visibility,
            "adult_content": community.adult_content,
            "topics": community.topics,
            "members": [community.created_by],  # Creator is the first member
            "moderators": [community.created_by],  # Creator is the first mod
            "created_at": datetime.utcnow().isoformat()
        })
        
        return {"message": "Community created successfully", "community_id": community_id}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/create_post")
def create_post(post: Post):
    try:
        # Generate unique Post ID
        post_id = str(uuid.uuid4())
        post_ref = db.collection("posts").document(post_id)
        
        # Verify that the community exists
        community_ref = db.collection("communities").document(post.community_id)
        community = community_ref.get()
        
        if not community.exists:
            raise HTTPException(status_code=404, detail="Community not found")
        
        # Prepare post data
        post_data = post.dict()
        post_data.update({
            "id": post_id,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
            "upvotes": 0,
            "downvotes": 0,
            "comment_count": 0,
        })
        
        # Handle specific post types
        if post.post_type == "poll" and post.poll_options:
            # Initialize vote counts for each option
            poll_results = {option: 0 for option in post.poll_options}
            post_data["poll_results"] = poll_results
        
        # Store post in Firestore
        post_ref.set(post_data)
        
        # Update post count in community
        community_data = community.to_dict()
        current_post_count = community_data.get("post_count", 0)
        community_ref.update({"post_count": current_post_count + 1})
        
        return {"message": "Post created successfully", "post_id": post_id}
    
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/add_comment")
def add_comment(comment: Comment):
    try:
        # Generate unique Comment ID
        comment_id = str(uuid.uuid4())
        comment_ref = db.collection("comments").document(comment_id)
        
        # Verify that the post exists
        post_ref = db.collection("posts").document(comment.post_id)
        post = post_ref.get()
        
        if not post.exists:
            raise HTTPException(status_code=404, detail="Post not found")
        
        # If it's a reply, verify that the parent comment exists
        if comment.parent_id:
            parent_comment_ref = db.collection("comments").document(comment.parent_id)
            parent_comment = parent_comment_ref.get()
            
            if not parent_comment.exists:
                raise HTTPException(status_code=404, detail="Parent comment not found")
        
        # Store comment in Firestore
        comment_ref.set({
            "id": comment_id,
            "post_id": comment.post_id,
            "parent_id": comment.parent_id,
            "author": comment.author,
            "content": comment.content,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
            "upvotes": 0,
            "downvotes": 0,
        })
        
        # Update comment count in post
        post_data = post.to_dict()
        current_comment_count = post_data.get("comment_count", 0)
        post_ref.update({"comment_count": current_comment_count + 1})
        
        return {"message": "Comment added successfully", "comment_id": comment_id}
    
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@app.post("/vote")
def vote(vote_data: Vote):
    try:
        # Check if post exists
        post_ref = db.collection("posts").document(vote_data.post_id)
        post = post_ref.get()

        if not post.exists:
            raise HTTPException(status_code=404, detail="Post not found")

        # Check if user has already voted
        votes_ref = db.collection("votes")
        existing_vote = votes_ref.where("post_id", "==", vote_data.post_id).where("user_id", "==", vote_data.user_id).get()

        post_data = post.to_dict()
        current_upvotes = post_data.get("upvotes", 0)
        current_downvotes = post_data.get("downvotes", 0)

        if existing_vote:
            existing_vote_id = existing_vote[0].id
            existing_vote_data = existing_vote[0].to_dict()
            existing_vote_type = existing_vote_data.get("vote_type")

            if existing_vote_type == vote_data.vote_type:
                # User is removing their vote
                if vote_data.vote_type == "upvote":
                    post_ref.update({"upvotes": max(0, current_upvotes - 1)})
                else:
                    post_ref.update({"downvotes": max(0, current_downvotes - 1)})

                votes_ref.document(existing_vote_id).delete()
            else:
                # User is switching their vote
                if vote_data.vote_type == "upvote":
                    post_ref.update({"upvotes": current_upvotes + 1, "downvotes": max(0, current_downvotes - 1)})
                else:
                    post_ref.update({"upvotes": max(0, current_upvotes - 1), "downvotes": current_downvotes + 1})

                votes_ref.document(existing_vote_id).update({"vote_type": vote_data.vote_type, "updated_at": datetime.utcnow().isoformat()})
        else:
            # New vote
            vote_id = str(uuid.uuid4())

            if vote_data.vote_type == "upvote":
                post_ref.update({"upvotes": current_upvotes + 1})
            else:
                post_ref.update({"downvotes": current_downvotes + 1})

            votes_ref.document(vote_id).set({
                "id": vote_id,
                "post_id": vote_data.post_id,
                "user_id": vote_data.user_id,
                "vote_type": vote_data.vote_type,
                "created_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat()
            })

        # Fetch the updated vote count after voting
        updated_post = post_ref.get().to_dict()
        return {
            "upvotes": updated_post.get("upvotes", 0),
            "downvotes": updated_post.get("downvotes", 0)
        }

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get all communities
@app.get("/get_communities")
def get_communities():
    try:
        communities_ref = db.collection("communities").stream()
        communities = [doc.to_dict() for doc in communities_ref]
        return communities
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get all posts
@app.get("/get_posts")
def get_posts():
    try:
        posts_ref = db.collection("posts").stream()
        posts = [doc.to_dict() for doc in posts_ref]
        return posts
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get posts by community
@app.get("/get_community_posts/{community_id}")
def get_community_posts(community_id: str):
    try:
        # Verify that the community exists
        community_ref = db.collection("communities").document(community_id)
        community = community_ref.get()
        
        if not community.exists:
            raise HTTPException(status_code=404, detail="Community not found")
        
        # Get posts for this community
        posts_ref = db.collection("posts").where("community_id", "==", community_id).stream()
        posts = [doc.to_dict() for doc in posts_ref]
        
        return posts
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get a single post with its comments
@app.get("/get_post/{post_id}")
def get_post(post_id: str):
    try:
        # Get the post
        post_ref = db.collection("posts").document(post_id)
        post = post_ref.get()
        
        if not post.exists:
            raise HTTPException(status_code=404, detail="Post not found")
        
        post_data = post.to_dict()
        
        # Get comments for this post
        comments_ref = db.collection("comments").where("post_id", "==", post_id).stream()
        comments = [doc.to_dict() for doc in comments_ref]
        
        # Organize comments into a hierarchy
        comment_dict = {comment["id"]: comment for comment in comments}
        comment_tree = []
        
        for comment in comments:
            if comment.get("parent_id") is None:
                # This is a root comment
                comment_tree.append(comment)
            else:
                # This is a reply
                parent_id = comment.get("parent_id")
                if parent_id in comment_dict:
                    if "replies" not in comment_dict[parent_id]:
                        comment_dict[parent_id]["replies"] = []
                    comment_dict[parent_id]["replies"].append(comment)
        
        # Return post with its comments
        return {
            "post": post_data,
            "comments": comment_tree
        }
    
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Join a community
@app.post("/join_community/{community_id}")
def join_community(community_id: str, user_email: str):
    try:
        # Verify that the community exists
        community_ref = db.collection("communities").document(community_id)
        community = community_ref.get()
        
        if not community.exists:
            raise HTTPException(status_code=404, detail="Community not found")
        
        community_data = community.to_dict()
        current_members = community_data.get("members", [])
        
        # Check if user is already a member
        if user_email in current_members:
            return {"message": "Already a member of this community"}
        
        # Add user to members
        current_members.append(user_email)
        community_ref.update({"members": current_members})
        
        return {"message": "Successfully joined community"}
    
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get a user's joined communities
@app.get("/get_user_communities/{user_email}")
def get_user_communities(user_email: str):
    try:
        # Get communities where user is a member
        communities_ref = db.collection("communities").where("members", "array_contains", user_email).stream()
        communities = [doc.to_dict() for doc in communities_ref]
        
        return communities
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get user profile
@app.get("/get_user/{user_id}")
def get_user(user_id: str):
    try:
        user_ref = db.collection("users").document(user_id)
        user = user_ref.get()
        
        if not user.exists:
            raise HTTPException(status_code=404, detail="User not found")
        
        user_data = user.to_dict()
        # Remove password from response
        if "password" in user_data:
            del user_data["password"]
            
        return user_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Search communities and posts
@app.get("/search")
def search(query: str):
    try:
        results = {
            "communities": [],
            "posts": []
        }
        
        # Search communities
        communities_ref = db.collection("communities").stream()
        for doc in communities_ref:
            community = doc.to_dict()
            if (query.lower() in community.get("name", "").lower() or 
                query.lower() in community.get("description", "").lower()):
                results["communities"].append(community)
        
        # Search posts
        posts_ref = db.collection("posts").stream()
        for doc in posts_ref:
            post = doc.to_dict()
            if (query.lower() in post.get("title", "").lower() or 
                query.lower() in post.get("content", "").lower()):
                results["posts"].append(post)
        
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))