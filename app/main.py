from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import voters, users, auth, general, booth_summaries, schemes
from app.core.middleware import RoleAccessMiddleware
from app.data.connection import close_db_connections

app = FastAPI(title="Voter Management System")

origins = [
    "http://localhost:3000",   # React dev
    "http://127.0.0.1:3000",
    "*"                        # Allow all for testing
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(RoleAccessMiddleware)

# Register routes
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(voters.router, prefix="/voters", tags=["Voters"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(general.router, prefix="/general", tags=["General"])
app.include_router(booth_summaries.router, prefix="/booth-summaries", tags=["Booth Summaries"])
app.include_router(schemes.router, prefix="/schemes", tags=["Schemes"])

@app.get("/")
def root():
    return {"message": "Voter Management Backend is running"}

@app.on_event("shutdown")
async def shutdown_event():
    close_db_connections()
