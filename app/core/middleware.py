from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from app.api.deps import get_constituency_file, fetch_user_from_token

ROLE_PERMISSIONS = {
    "super_admin": ["*"],
    "admin": ["*"],
    "booth_volunteer": ["/voters", "/voters/{epic_id}"],
    "panchayat_prabhari": ["*"],
    "block_prabhari": ["*"],
    "vidhan_sabha_prabhari": ["*"],
    "candidate": ["*"],
    "political_party": ["*"]
}

EXCLUDED_PATHS = [
    "/auth/login",
    "/auth/forgot-password",
    "/auth/reset-password"
]

class RoleAccessMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Skip login route
        if any(request.url.path.startswith(path) for path in EXCLUDED_PATHS):
            return await call_next(request)

        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return JSONResponse(status_code=401, content={"detail": "Missing or invalid Authorization header"})

        token = auth_header.split(" ")[1]

        constituency_file = get_constituency_file()  # sync call, adjust if async

        try:
            user = await fetch_user_from_token(token, constituency_file)
        except HTTPException:
            return JSONResponse(status_code=401, content={"detail": "Invalid token"})

        allowed_paths = ROLE_PERMISSIONS.get(user.role, [])
        if "*" not in allowed_paths and not any(request.url.path.startswith(p) for p in allowed_paths):
            return JSONResponse(status_code=403, content={"detail": "Role not allowed to access this endpoint"})

        response = await call_next(request)
        return response
