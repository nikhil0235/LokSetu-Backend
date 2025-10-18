from fastapi import APIRouter, Depends, HTTPException, Form, BackgroundTasks
from datetime import datetime, timedelta
from jose import jwt, JWTError
from app.core.config import settings
from app.services.user_service import UserService
from app.core.security import hash_password
from app.utils.email_sender import send_email
import os
import glob

router = APIRouter()

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 480

@router.post("/login")
def login(
    username: str = Form(...),
    password: str = Form(...)
):
    user_service = UserService()
    user = user_service.authenticate_user(username, password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    token = jwt.encode(
        {"sub": user["username"], "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)},
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    
    return {
        "access_token": token, 
        "token_type": "bearer",
        "fullname": user["full_name"],
        "username": user["username"],
        "role": user["role"],
        "assigned_booths_ids": user["assigned_booths"],
        "assigned_constituencies_ids": user["assigned_constituencies"],
        "user_id": user["user_id"],
        "phone": user["phone"],
        "email": user["email"],
        "created_by": user["created_by"]
    }


@router.post("/forgot-password")
def forgot_password(
    background_tasks: BackgroundTasks,
    username: str = Form(...)
):
    service = UserService()
    user = service.get_user_by_username(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not user.email:
        raise HTTPException(status_code=400, detail="No email registered for this user")

    token_data = {"sub": username}
    reset_token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
    print(reset_token)
    # Email content
    reset_link = f"http://frontend-app/reset-password?token={reset_token}"
    email_body = f"""
    <p>Hello {user.full_name or user.username},</p>
    <p>You requested to reset your password. Click the link below to set a new one:</p>
    <a href="{reset_link}">{reset_link}</a>
    <p>This link expires in {ACCESS_TOKEN_EXPIRE_MINUTES} minutes.</p>
    """

    # Send email in background
    background_tasks.add_task(send_email, user.email, "Password Reset Request", email_body)

    return {"message": f"Password reset instructions sent to {user.email}"}


@router.post("/reset-password")
def reset_password(token: str = Form(...), new_password: str = Form(...)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=400, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    service = UserService()
    user = service.get_user_by_username(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Update password in Excel
    service.update_user_password(username, hash_password(new_password))
    return {"message": "Password reset successful"}
