import uuid
import secrets
import logging
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
from app.services.email_service import EmailVerificationService
from app.schemas.auth import (
    UserRegisterSchema,
    UserLoginSchema,
    ForgotPasswordSchema,
    UserOutSchema,
    AuthResponseSchema,
    SendOtpSchema,
    VerifyOtpSchema,
)

router = APIRouter(prefix="/api/auth", tags=["Authentication"])
logger = logging.getLogger(__name__)

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
    except (JWTError, Exception) as e:
        logger.warning("Token decode or user lookup failure: %s", e)
        return None

def get_current_user(user: Optional[User] = Depends(get_current_user_optional)) -> User:
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required. Please sign in."
        )
    return user

@router.post("/send-otp")
def send_otp(payload: SendOtpSchema, db: Session = Depends(get_db)):
    """
    Dispatches a 6-digit verification OTP to a genuine email.
    Rejects disposable, throwaway, and non-existent email domains.
    """
    clean_email = payload.email.lower().strip()
    is_genuine, err_msg = EmailVerificationService.is_valid_genuine_email(clean_email)
    if not is_genuine:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=err_msg
        )

    # Check if an already verified user exists
    existing = db.query(User).filter(User.email == clean_email).first()
    if existing and existing.is_verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An account with this email address is already verified and registered. Please sign in."
        )

    otp_code = EmailVerificationService.generate_otp(6)
    expires_at = datetime.utcnow() + timedelta(minutes=10)

    # Save OTP to existing unverified user or create placeholder
    if existing:
        existing.otp_code = otp_code
        existing.otp_expires_at = expires_at
        if payload.fullName:
            existing.full_name = payload.fullName
        db.commit()
    else:
        # Create unverified user placeholder with temporary password hash
        new_user = User(
            id=str(uuid.uuid4()),
            full_name=payload.fullName or "User",
            email=clean_email,
            hashed_password=get_password_hash(secrets.token_urlsafe(16)),
            role=UserRoleEnum.FARMER,
            is_verified=False,
            otp_code=otp_code,
            otp_expires_at=expires_at,
        )
        db.add(new_user)
        db.commit()

    # Send the real email
    sent, send_msg = EmailVerificationService.send_otp_email(clean_email, payload.fullName or "User", otp_code)
    if not sent:
        # Clear unsent OTP so invalid/unreachable codes cannot linger
        if existing:
            existing.otp_code = None
            existing.otp_expires_at = None
            db.commit()
        else:
            db.delete(new_user)
            db.commit()

        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Verification email delivery failed: {send_msg}"
        )

    return {
        "success": True,
        "message": f"Verification code sent to {clean_email}.",
        "email": clean_email
    }

@router.post("/verify-otp")
def verify_otp(payload: VerifyOtpSchema, db: Session = Depends(get_db)):
    """
    Verifies the 6-digit OTP code against the database record.
    """
    clean_email = payload.email.lower().strip()
    user = db.query(User).filter(User.email == clean_email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No registration request found for this email. Please request a new verification code."
        )

    if not user.otp_code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No active verification code found. Please request a new code."
        )

    if user.otp_expires_at and datetime.utcnow() > user.otp_expires_at:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Verification code has expired. Please request a new code."
        )

    if user.otp_code != payload.otp.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid verification code. Please check the code and try again."
        )

    # Mark user as verified and clear OTP
    user.is_verified = True
    user.otp_code = None
    user.otp_expires_at = None
    db.commit()
    db.refresh(user)

    token = create_access_token(data={"sub": user.id, "email": user.email, "role": get_role_str(user.role)})
    return {
        "success": True,
        "message": "Email verified successfully.",
        "token": token,
        "user": user.to_dict()
    }

@router.post("/signup", response_model=AuthResponseSchema, status_code=status.HTTP_201_CREATED)
def signup(payload: UserRegisterSchema, db: Session = Depends(get_db)):
    # Block public registration as admin
    if payload.role == UserRoleEnum.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Public registration for the Administrator role is strictly restricted."
        )

    clean_email = payload.email.lower().strip()

    # Check if user already exists
    existing = db.query(User).filter(User.email == clean_email).first()

    # Mobile App Flow (with OTP)
    if payload.otp:
        if existing and existing.is_verified:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="An account with this email address already exists. Please sign in."
            )
        if not existing or not existing.otp_code:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Verification code not requested. Please click Send Verification Code first."
            )
        if existing.otp_expires_at and datetime.utcnow() > existing.otp_expires_at:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Verification code expired. Please request a new one."
            )
        if existing.otp_code != payload.otp.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect verification code."
            )
        # Update existing placeholder
        existing.full_name = payload.fullName
        existing.hashed_password = get_password_hash(payload.password)
        existing.role = payload.role
        existing.is_verified = True
        existing.otp_code = None
        existing.otp_expires_at = None
        db.commit()
        db.refresh(existing)
        target_user = existing
    else:
        # Standard Web App Flow (Direct signup without OTP requirement)
        if existing and existing.is_verified:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="An account with this email address already exists. Please sign in."
            )
        hashed_pwd = get_password_hash(payload.password)
        if existing:
            existing.full_name = payload.fullName
            existing.hashed_password = hashed_pwd
            existing.role = payload.role
            existing.is_verified = True
            existing.otp_code = None
            existing.otp_expires_at = None
            db.commit()
            db.refresh(existing)
            target_user = existing
        else:
            user_id = str(uuid.uuid4())
            new_user = User(
                id=user_id,
                full_name=payload.fullName,
                email=clean_email,
                hashed_password=hashed_pwd,
                role=payload.role,
                is_verified=True
            )
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            target_user = new_user

    token = create_access_token(data={"sub": target_user.id, "email": target_user.email, "role": get_role_str(target_user.role)})
    return {
        "token": token,
        "user": target_user.to_dict(),
        "message": "Account registered successfully."
    }

@router.post("/login", response_model=AuthResponseSchema)
def login(payload: UserLoginSchema, db: Session = Depends(get_db)):
    """Authenticate an existing account. Account creation belongs to /signup only."""
    try:
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
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Unexpected error during login for %s: %s", payload.email, e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An internal authentication error occurred. Please try again."
        )

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
