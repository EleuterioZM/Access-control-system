from fastapi import APIRouter, status
from pydantic import BaseModel
from datetime import datetime
from typing import List

router = APIRouter(prefix="/audit", tags=["Audit"])

class AuditLog(BaseModel):
    user: str
    action: str
    time: str

logs_list: List[AuditLog] = [
    AuditLog(user="admin", action="Login", time=datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
]

@router.get("/", response_model=List[AuditLog])
def get_logs():
    return logs_list

@router.post("/add", response_model=AuditLog, status_code=status.HTTP_201_CREATED)
def add_log(user: str, action: str):
    new_log = AuditLog(user=user, action=action, time=datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    logs_list.append(new_log)
    return new_log
