from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
import jwt
from datetime import datetime, timedelta

router = APIRouter()

# Secret key for JWT token generation
SECRET_KEY = "your_secret_key"  # Change this in production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Simple in-memory user database (in production, use a real database)
fake_users_db = {
    "user1": {
        "username": "user1",
        "password": "password1",
    }
}

class Token(BaseModel):
    token: str
    userId: str
    username: str

class LoginRequest(BaseModel):
    username: str
    password: str

class RegisterRequest(BaseModel):
    username: str
    password: str

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@router.post("/login")
async def login(login_request: LoginRequest):
    user = fake_users_db.get(login_request.username)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username")
    if user["password"] != login_request.password:
        raise HTTPException(status_code=401, detail="Invalid password")
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    
    return Token(token=access_token, userId=user["username"], username=user["username"])

@router.post("/register")
async def register(register_request: RegisterRequest):
    if register_request.username in fake_users_db:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    # Store new user
    fake_users_db[register_request.username] = {
        "username": register_request.username,
        "password": register_request.password,
    }
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": register_request.username}, expires_delta=access_token_expires
    )
    
    return Token(token=access_token, userId=register_request.username, username=register_request.username)