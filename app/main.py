from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import voters, users, auth, general, booth_summaries, schemes, parties
from app.core.middleware import RoleAccessMiddleware
from app.core.exceptions import global_exception_handler
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

# Add global exception handler
app.add_exception_handler(Exception, global_exception_handler)

# Register routes
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(voters.router, prefix="/voters", tags=["Voters"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(general.router, prefix="/general", tags=["General"])
app.include_router(booth_summaries.router, prefix="/booth-summaries", tags=["Booth Summaries"])
app.include_router(schemes.router, prefix="/schemes", tags=["Schemes"])
app.include_router(parties.router, prefix="/parties", tags=["Parties"])

@app.get("/")
def root():
    return {"message": "Voter Management Backend is running"}

@app.on_event("shutdown")
async def shutdown_event():
    close_db_connections()
