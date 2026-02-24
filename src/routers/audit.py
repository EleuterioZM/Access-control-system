from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from datetime import datetime
from typing import List

router = APIRouter(prefix="/audit", tags=["Audit"])
templates = Jinja2Templates(directory="src/templates")

# Modelo de log de auditoria
class AuditLog(BaseModel):
    user: str
    action: str
    time: str

# Lista simulada de logs de auditoria
logs_list: List[AuditLog] = [
    AuditLog(user="admin", action="Login", time=datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
]


# Endpoint HTML

@router.get("/", response_class=None)
def list_logs(request: Request):
    """Exibe os logs na página HTML"""
    return templates.TemplateResponse("audit.html", {"request": request, "logs": logs_list})


# Endpoints REST

@router.get("/all", response_model=List[AuditLog])
def get_logs():
    """Retorna todos os logs em JSON"""
    return logs_list

@router.post("/add", response_model=AuditLog, status_code=status.HTTP_201_CREATED)
def add_log(user: str, action: str):
    """Adiciona um novo log"""
    new_log = AuditLog(user=user, action=action, time=datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    logs_list.append(new_log)
    return new_log
