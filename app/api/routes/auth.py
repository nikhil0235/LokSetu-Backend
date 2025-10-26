from fastapi import APIRouter, Depends, HTTPException, Form, BackgroundTasks
from datetime import datetime, timedelta
from jose import jwt, JWTError
from app.core.config import settings
from app.services.user_service import UserService
from app.services.otp_service import OTPService
from app.core.security import hash_password
from app.utils.email_sender import send_email
from app.schemas.auth_schema import MobileLoginRequest, OTPVerifyRequest, LoginResponse, OTPResponse
from app.utils.logger import logger

router = APIRouter()

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 480

@router.post("/login")
def login(
    username: str = Form(...),
    password: str = Form(...)
):
    try:
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
            "assigned_blocks_ids": user["assigned_blocks"],
            "assigned_panchayats_ids": user["assigned_panchayats"],
            "user_id": user["user_id"],
            "phone": user["phone"],
            "email": user["email"],
            "created_by": user["created_by"],
            "party_id": user.get("party_id"),
            "alliance_id": user.get("alliance_id"),
            "party_name": user.get("party_name"),
            "alliance_name": user.get("alliance_name")
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error for user {username}: {str(e)}")
        raise HTTPException(status_code=500, detail="Login failed. Please try again later.")


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

@router.post("/send-otp", response_model=OTPResponse)
def send_otp(request: MobileLoginRequest):
    """Send OTP to mobile number"""
    user_service = UserService()
    user = user_service.get_user_by_mobile(request.mobile)
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found with this mobile number")
    
    otp_service = OTPService()
    success, otp_ = otp_service.send_otp(request.mobile)
    
    if not success:
        raise HTTPException(status_code=500, detail="Failed to send OTP")
    
    return OTPResponse(message="OTP sent successfully", expires_in=300, otp=otp_)

@router.post("/verify-otp", response_model=LoginResponse)
def verify_otp(request: OTPVerifyRequest):
    """Verify OTP and login user"""
    user_service = UserService()
    user = user_service.get_user_by_mobile(request.mobile)
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    otp_service = OTPService()
    if not otp_service.verify_otp(request.mobile, request.otp):
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")
    
    # Generate JWT token
    token = jwt.encode(
        {"sub": user["username"], "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)},
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    
    return LoginResponse(
        access_token=token,
        token_type="bearer",
        fullname=user["full_name"],
        username=user["username"],
        role=user["role"],
        assigned_booths_ids=user["assigned_booths"],
        assigned_constituencies_ids=user["assigned_constituencies"],
        assigned_blocks_ids=user["assigned_blocks"],
        assigned_panchayats_ids=user["assigned_panchayats"],
        user_id=user["user_id"],
        phone=user["phone"],
        email=user["email"],
        created_by=user["created_by"],
        party_id=user.get("party_id"),
        alliance_id=user.get("alliance_id"),
        party_name=user.get("party_name"),
        alliance_name=user.get("alliance_name")
    )
