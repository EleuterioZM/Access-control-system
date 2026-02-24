from fastapi import APIRouter, Request, Form, Response, status, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from src.database.session import SessionLocal
from src.models.user import User
from passlib.context import CryptContext

router = APIRouter()
templates = Jinja2Templates(directory="src/templates")
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# LOGIN

@router.get("/login")
def login_get(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login")
def login_post(
    request: Request, 
    response: Response, 
    username: str = Form(...), 
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == username).first()
    if user and verify_password(password, user.password):
        # Cria cookie de sessão
        response = RedirectResponse(url="/dashboard", status_code=status.HTTP_302_FOUND)
        response.set_cookie(key="user", value=username)
        return response
    else:
        return templates.TemplateResponse("login.html", {"request": request, "error": "Usuário ou senha incorretos"})

# REGISTER (Open registration for testing, usually restricted)

@router.get("/register")
def register_get(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@router.post("/register")
def register_post(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    full_name: str = Form(...), # Not in model yet, but let's keep it in form
    email: str = Form(...),
    role: str = Form(...),
    db: Session = Depends(get_db)
):
    if db.query(User).filter(User.username == username).first():
        return templates.TemplateResponse("register.html", {"request": request, "error": "Usuário já existe"})
    
    hashed_password = pwd_context.hash(password)
    novo_usuario = User(
        username=username,
        email=email,
        password=hashed_password,
        role=role
    )
    db.add(novo_usuario)
    db.commit()
    return RedirectResponse(url="/auth/login", status_code=status.HTTP_302_FOUND)
