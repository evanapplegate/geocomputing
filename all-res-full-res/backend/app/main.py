from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth, posts, users
from app.config import settings

app = FastAPI(title="All Res Full Res API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url, "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(posts.router)
app.include_router(users.router)


@app.get("/")
async def root():
    return {"message": "All Res Full Res API"}


@app.get("/health")
async def health():
    return {"status": "ok"}
