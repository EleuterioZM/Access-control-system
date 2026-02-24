from fastapi import APIRouter
from typing import List, Dict

router = APIRouter(prefix="/roles", tags=["Roles"])

roles_list = [{"id": 1, "name": "Administrador"}, {"id": 2, "name": "Usuário"}]

@router.get("/")
def list_roles():
    return roles_list

@router.post("/add")
def add_role(name: str):
    new_id = len(roles_list) + 1
    new_role = {"id": new_id, "name": name}
    roles_list.append(new_role)
    return new_role

@router.delete("/{role_id}")
def delete_role(role_id: int):
    global roles_list
    roles_list = [r for r in roles_list if r["id"] != role_id]
    return {"message": "Role deleted"}
