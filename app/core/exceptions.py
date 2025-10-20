from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from app.utils.logger import logger
import traceback

async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler for unhandled exceptions"""
    
    # Log the full error details
    logger.error(f"Unhandled exception: {str(exc)}")
    logger.error(f"Request URL: {request.url}")
    logger.error(f"Traceback: {traceback.format_exc()}")
    
    # Database connection errors
    if "connection" in str(exc).lower() or "database" in str(exc).lower():
        return JSONResponse(
            status_code=503,
            content={
                "error": "Database connection error",
                "message": "Unable to connect to database. Please try again later.",
                "type": "database_error"
            }
        )
    
    # Unique constraint violations - phone/email duplicates
    if "unique constraint" in str(exc).lower() or "duplicate key" in str(exc).lower():
        error_msg = str(exc).lower()
        if "phone" in error_msg:
            return JSONResponse(
                status_code=400,
                content={
                    "error": "Duplicate phone number",
                    "message": "This phone number is already registered with another user.",
                    "type": "duplicate_phone"
                }
            )
        elif "email" in error_msg:
            return JSONResponse(
                status_code=400,
                content={
                    "error": "Duplicate email",
                    "message": "This email address is already registered with another user.",
                    "type": "duplicate_email"
                }
            )
        elif "username" in error_msg:
            return JSONResponse(
                status_code=400,
                content={
                    "error": "Duplicate username",
                    "message": "This username is already taken. Please choose a different one.",
                    "type": "duplicate_username"
                }
            )
    
    # Foreign key constraint errors
    if "foreign key" in str(exc).lower() or "violates" in str(exc).lower():
        return JSONResponse(
            status_code=400,
            content={
                "error": "Data integrity error",
                "message": "The operation violates data constraints. Please check your input.",
                "type": "constraint_error"
            }
        )
    
    # Validation errors
    if "validation" in str(exc).lower() or "invalid" in str(exc).lower():
        return JSONResponse(
            status_code=400,
            content={
                "error": "Validation error",
                "message": "Invalid input data provided.",
                "type": "validation_error"
            }
        )
    
    # Permission/Authentication errors
    if "permission" in str(exc).lower() or "unauthorized" in str(exc).lower():
        return JSONResponse(
            status_code=403,
            content={
                "error": "Permission denied",
                "message": "You don't have permission to perform this action.",
                "type": "permission_error"
            }
        )
    
    # Generic server error
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": "An unexpected error occurred. Please try again later.",
            "type": "server_error"
        }
    )