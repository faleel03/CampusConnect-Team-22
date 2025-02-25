from fastapi import APIRouter, HTTPException
from backend.security import hash_password, verify_password
from backend.database import users_collection  # Firestore collection for users
from backend.models import UserCreate, UserLogin  # Pydantic models

auth_router = APIRouter()

@auth_router.post("/register")
async def register(user: UserCreate):
    existing_user = users_collection.document(user.email).get()
    if existing_user.exists:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_password = hash_password(user.password)
    users_collection.document(user.email).set({
        "email": user.email,
        "password": hashed_password
    })
    return {"message": "User registered successfully"}

@auth_router.post("/login")
async def login(user: UserLogin):
    stored_user = users_collection.document(user.email).get()
    if not stored_user.exists:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    user_data = stored_user.to_dict()
    if not verify_password(user.password, user_data["password"]):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    return {"message": "Login successful"}