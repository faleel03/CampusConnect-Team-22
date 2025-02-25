from fastapi import APIRouter, HTTPException, Depends
from backend.security import hash_password, verify_password
from backend.database import users_collection  # Firestore collection for users
from backend.models import UserCreate, UserLogin  # Pydantic models

from typing import List

users_router = APIRouter()

@users_router.get("/users", response_model=List[UserCreate])
async def get_all_users():
    users = users_collection.stream()
    return [{"email": user.id, "password": user.to_dict()["password"]} for user in users]

@users_router.get("/users/{email}")
async def get_user(email: str):
    user = users_collection.document(email).get()
    if not user.exists:
        raise HTTPException(status_code=404, detail="User not found")
    return user.to_dict()

@users_router.put("/users/{email}")
async def update_user(email: str, user: UserCreate):
    existing_user = users_collection.document(email).get()
    if not existing_user.exists:
        raise HTTPException(status_code=404, detail="User not found")

    hashed_password = hash_password(user.password)
    users_collection.document(email).update({"password": hashed_password})
    return {"message": "User updated successfully"}

@users_router.delete("/users/{email}")
async def delete_user(email: str):
    existing_user = users_collection.document(email).get()
    if not existing_user.exists:
        raise HTTPException(status_code=404, detail="User not found")

    users_collection.document(email).delete()
    return {"message": "User deleted successfully"}