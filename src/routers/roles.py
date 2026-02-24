from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/roles", tags=["Roles"])
templates = Jinja2Templates(directory="src/templates")

# Lista simulada de roles
roles_list = [{"id": 1, "name": "Administrador"}, {"id": 2, "name": "Usuário"}]

# Listar roles (HTML)
@router.get("/", response_class=None)
def list_roles(request: Request):
    return templates.TemplateResponse("roles.html", {"request": request, "roles": roles_list})

# Adicionar role
@router.post("/add")
def add_role(name: str = Form(...)):
    new_id = len(roles_list) + 1
    roles_list.append({"id": new_id, "name": name})
    return RedirectResponse(url="/roles/", status_code=303)

# Remover role
@router.post("/delete")
def delete_role(role_id: int = Form(...)):
    global roles_list
    roles_list = [r for r in roles_list if r["id"] != role_id]
    return RedirectResponse(url="/roles/", status_code=303)
