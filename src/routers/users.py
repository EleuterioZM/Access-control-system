from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import List, Dict

router = APIRouter()
templates = Jinja2Templates(directory="src/templates")

# Banco simulado de usuários
fake_users: List[Dict] = [
    {"fullname": "Admin User", "email": "admin@example.com", "username": "admin", "role": "Administrator"}
]

# Listar usuários
@router.get("/")
def list_users(request: Request):
    return templates.TemplateResponse("users.html", {"request": request, "users": fake_users})

# Adicionar usuário
@router.post("/add")
def add_user(
    fullname: str = Form(...),
    email: str = Form(...),
    username: str = Form(...),
    role: str = Form(...)
):
    fake_users.append({
        "fullname": fullname,
        "email": email,
        "username": username,
        "role": role
    })
    return RedirectResponse(url="/users/", status_code=302)

# Remover usuário
@router.post("/delete")
def delete_user(username: str = Form(...)):
    global fake_users
    fake_users = [u for u in fake_users if u["username"] != username]
    return RedirectResponse(url="/users/", status_code=302)

# Editar usuário (GET para exibir formulário)
@router.get("/edit")
def edit_user_get(request: Request, username: str):
    user = next((u for u in fake_users if u["username"] == username), None)
    if not user:
        return RedirectResponse(url="/users/")
    return templates.TemplateResponse("edit_user.html", {"request": request, "user": user})

# Editar usuário (POST para salvar)
@router.post("/edit")
def edit_user_post(
    fullname: str = Form(...),
    email: str = Form(...),
    username: str = Form(...),
    role: str = Form(...)
):
    for u in fake_users:
        if u["username"] == username:
            u["fullname"] = fullname
            u["email"] = email
            u["role"] = role
            break
    return RedirectResponse(url="/users/", status_code=302)
