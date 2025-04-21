from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from app.auth.routes import router as auth_router
from app.audio.routes import router as audio_router

app = FastAPI(title="Audio Emotion Analyzer API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development, in production specify domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(audio_router, prefix="/audio", tags=["Audio Processing"])

@app.get("/")
def read_root():
    return {"message": "Welcome to Audio Emotion Analyzer API"}