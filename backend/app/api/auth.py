import uuid
from typing import Optional
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import bcrypt
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer

from app.database import get_db
from app.config import settings
from app.models.user import User, UserRoleEnum
from app.schemas.auth import (
    UserRegisterSchema,
    UserLoginSchema,
    ForgotPasswordSchema,
    UserOutSchema,
    AuthResponseSchema,
)

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login", auto_error=False)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return bcrypt.checkpw(
            plain_password.encode("utf-8")[:72],
            hashed_password.encode("utf-8")
        )
    except Exception:
        return False

def get_password_hash(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8")[:72], salt).decode("utf-8")

def get_role_str(role) -> str:
    if hasattr(role, "value"):
        return str(role.value)
    return str(role)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

def get_current_user_optional(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> Optional[User]:
    if not token:
        return None
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        user_id: str = payload.get("sub")
        if not user_id:
            return None
        return db.query(User).filter(User.id == user_id).first()
    except JWTError:
        return None

def get_current_user(user: Optional[User] = Depends(get_current_user_optional)) -> User:
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required. Please sign in."
        )
    return user

@router.post("/signup", response_model=AuthResponseSchema, status_code=status.HTTP_201_CREATED)
def signup(payload: UserRegisterSchema, db: Session = Depends(get_db)):
    # Block public registration as admin
    if payload.role == UserRoleEnum.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Public registration for the Administrator role is strictly restricted."
        )

    # Check if user already exists
    existing = db.query(User).filter(User.email == payload.email.lower()).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An account with this email address already exists. Please sign in."
        )

    user_id = str(uuid.uuid4())
    hashed_pwd = get_password_hash(payload.password)

    new_user = User(
        id=user_id,
        full_name=payload.fullName,
        email=payload.email.lower(),
        hashed_password=hashed_pwd,
        role=payload.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    token = create_access_token(data={"sub": new_user.id, "email": new_user.email, "role": get_role_str(new_user.role)})
    return {
        "token": token,
        "user": new_user.to_dict(),
        "message": "Account registered successfully."
    }

@router.post("/login", response_model=AuthResponseSchema)
def login(payload: UserLoginSchema, db: Session = Depends(get_db)):
    """Authenticate an existing account. Account creation belongs to /signup only."""
    email_clean = payload.email.lower().strip()
    user = db.query(User).filter(User.email == email_clean).first()

    # Never create an account during login: a typo or an attacker must not silently
    # create a new identity and make the UI appear to have authenticated an old one.
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password. If you are new to AGRO AI, create an account first."
        )

    token = create_access_token(data={"sub": user.id, "email": user.email, "role": get_role_str(user.role)})
    return {
        "token": token,
        "user": user.to_dict(),
        "message": "Authentication successful."
    }

@router.get("/me")
def get_me(user: Optional[User] = Depends(get_current_user_optional)):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not authenticated."
        )
    return {"user": user.to_dict()}

@router.post("/logout")
def logout():
    return {"message": "Logged out successfully."}

@router.post("/forgot-password")
def forgot_password(payload: ForgotPasswordSchema, db: Session = Depends(get_db)):
    # Safe response
    return {
        "message": f"If an account exists for {payload.email}, password recovery guidance has been dispatched."
    }
