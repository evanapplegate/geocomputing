from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.routes import auth, posts, users
from app.config import settings
from app.middleware import logging_middleware
from app.r2_storage import USE_LOCAL_STORAGE, LOCAL_MEDIA_ROOT, LOCAL_MEDIA_URL_BASE

app = FastAPI(title="All Res Full Res API")

# Logging middleware
app.middleware("http")(logging_middleware)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url, "http://localhost:3000", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(posts.router)
app.include_router(users.router)

if USE_LOCAL_STORAGE:
    LOCAL_MEDIA_ROOT.mkdir(parents=True, exist_ok=True)
    app.mount(LOCAL_MEDIA_URL_BASE, StaticFiles(directory=LOCAL_MEDIA_ROOT), name="local-media")


@app.get("/")
async def root():
    return {"message": "All Res Full Res API"}


@app.get("/health")
async def health():
    return {"status": "ok"}
