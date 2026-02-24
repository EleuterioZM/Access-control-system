import random
import secrets
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from datetime import datetime, timedelta
from src.database.session import SessionLocal
from src.models.user import User
from src.utils.mail import send_otp_email, send_reset_email
from passlib.context import CryptContext

router = APIRouter(prefix="/api", tags=["API"])

SECRET_KEY = "super-secret-key-for-jwt"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
OTP_EXPIRE_MINUTES = 10
RESET_EXPIRE_HOURS = 1

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/login")

class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    password: str

class OTPVerify(BaseModel):
    email: str
    otp_code: str
    pending_token: str

class ForgotPassword(BaseModel):
    email: EmailStr

class ResetPassword(BaseModel):
    email: EmailStr
    token: str
    new_password: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == user_in.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = pwd_context.hash(user_in.password)
    new_user = User(
        username=user_in.email,
        full_name=user_in.full_name,
        email=user_in.email,
        password=hashed_password,
        role="user"
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"id": new_user.id, "email": new_user.email, "message": "User created successfully"}

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not pwd_context.verify(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    
    # Gerar OTP de 4 dígitos
    otp = f"{random.randint(1000, 9999)}"
    user.otp_code = otp
    user.otp_expiry = datetime.utcnow() + timedelta(minutes=OTP_EXPIRE_MINUTES)
    db.commit()

    # Enviar Email
    sent = send_otp_email(user.email, otp)
    if not sent:
        raise HTTPException(status_code=500, detail="Error sending OTP email")

    # Retornar token pendente
    pending_token = create_token(data={"sub": user.email, "type": "otp_pending"}, expires_delta=timedelta(minutes=OTP_EXPIRE_MINUTES))
    
    return {
        "message": "OTP sent to your email",
        "email": user.email,
        "pending_token": pending_token
    }

@router.post("/verify-otp")
def verify_otp(data: OTPVerify, db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(data.pending_token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("sub") != data.email or payload.get("type") != "otp_pending":
            raise HTTPException(status_code=401, detail="Invalid pending token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid pending token")

    user = db.query(User).filter(User.email == data.email).first()
    if not user or user.otp_code != data.otp_code or datetime.utcnow() > user.otp_expiry:
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")

    # Limpar OTP após uso
    user.otp_code = None
    user.otp_expiry = None
    db.commit()

    # Retornar token de acesso final
    access_token = create_token(data={"sub": user.username, "role": user.role}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/forgot-password")
def forgot_password(data: ForgotPassword, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user:
        # Don't reveal if user exists
        return {"message": "If the email is registered, you will receive a reset link"}

    token = secrets.token_urlsafe(32)
    user.reset_token = token
    user.reset_token_expiry = datetime.utcnow() + timedelta(hours=RESET_EXPIRE_HOURS)
    db.commit()

    send_reset_email(user.email, token)
    return {"message": "Reset token sent to your email"}

@router.post("/reset-password")
def reset_password(data: ResetPassword, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email, User.reset_token == data.token).first()
    if not user or datetime.utcnow() > user.reset_token_expiry:
        raise HTTPException(status_code=400, detail="Invalid or expired reset token")

    user.password = pwd_context.hash(data.new_password)
    user.reset_token = None
    user.reset_token_expiry = None
    db.commit()
    return {"message": "Password updated successfully"}

@router.get("/me")
def read_users_me(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None or payload.get("type") == "otp_pending":
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": user.id, "username": user.username, "full_name": user.full_name, "email": user.email, "role": user.role}
