from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="src/templates")

# Dashboard com funções básicas para mostrar ao recrutador
@router.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    """
    Página principal do dashboard.
    Mostra usuários, roles e estatísticas fictícias.
    """
    # Dados de exemplo (para mostrar no dashboard)
    users = ["Admin", "Gabriel", "TestUser"]
    roles = ["Admin", "User", "Auditor"]
    stats = {"total_users": len(users), "total_roles": len(roles)}

    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request, "users": users, "roles": roles, "stats": stats}
    )
