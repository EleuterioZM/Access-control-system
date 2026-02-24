from sqlalchemy import Column, Integer, String, Boolean, DateTime
from src.database.base import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=True)
    email = Column(String, unique=True, index=True, nullable=True)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False, default="user")
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    
    # Advanced Auth
    otp_code = Column(String, nullable=True)
    otp_expiry = Column(DateTime, nullable=True)
    reset_token = Column(String, nullable=True)
    reset_token_expiry = Column(DateTime, nullable=True)
