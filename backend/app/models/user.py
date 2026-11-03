import enum
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Enum, Boolean
from app.database import Base

class UserRoleEnum(str, enum.Enum):
    FARMER = "farmer"
    BUYER = "buyer"
    GENERAL = "general"
    ADMIN = "admin"

class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, index=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(Enum(UserRoleEnum), default=UserRoleEnum.FARMER, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    otp_code = Column(String(10), nullable=True)
    otp_expires_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def get_role_value(self) -> str:
        if hasattr(self.role, "value"):
            return str(self.role.value)
        return str(self.role)

    def to_dict(self):
        return {
            "id": self.id,
            "fullName": self.full_name,
            "email": self.email,
            "role": self.get_role_value(),
            "isVerified": bool(self.is_verified),
            "createdAt": self.created_at.isoformat() if self.created_at else None,
        }
