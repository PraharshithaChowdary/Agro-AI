import re
from pydantic import BaseModel, Field, field_validator
from typing import Optional
from app.models.user import UserRoleEnum

EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

class SendOtpSchema(BaseModel):
    email: str = Field(..., min_length=5, max_length=150)
    fullName: Optional[str] = "User"

class VerifyOtpSchema(BaseModel):
    email: str = Field(..., min_length=5, max_length=150)
    otp: str = Field(..., min_length=6, max_length=6)

class UserRegisterSchema(BaseModel):
    fullName: str = Field(..., min_length=2, max_length=100)
    email: str = Field(..., min_length=5, max_length=150)
    password: str = Field(..., min_length=6, max_length=128)
    role: UserRoleEnum = UserRoleEnum.FARMER
    otp: Optional[str] = None

    @field_validator("email")
    @classmethod
    def validate_email_format(cls, v: str) -> str:
        clean = v.strip().lower()
        if not EMAIL_REGEX.match(clean):
            raise ValueError("Invalid email address format.")
        return clean

class UserLoginSchema(BaseModel):
    email: str = Field(..., min_length=5, max_length=150)
    password: str

    @field_validator("email")
    @classmethod
    def validate_email_format(cls, v: str) -> str:
        clean = v.strip().lower()
        if not EMAIL_REGEX.match(clean):
            raise ValueError("Invalid email address format.")
        return clean

class ForgotPasswordSchema(BaseModel):
    email: str = Field(..., min_length=5, max_length=150)

    @field_validator("email")
    @classmethod
    def validate_email_format(cls, v: str) -> str:
        clean = v.strip().lower()
        if not EMAIL_REGEX.match(clean):
            raise ValueError("Invalid email address format.")
        return clean

class UserOutSchema(BaseModel):
    id: str
    fullName: str
    email: str
    role: str
    isVerified: Optional[bool] = False
    createdAt: Optional[str] = None

class AuthResponseSchema(BaseModel):
    token: str
    user: UserOutSchema
    message: Optional[str] = None
