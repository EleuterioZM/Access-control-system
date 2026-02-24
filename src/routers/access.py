from fastapi import APIRouter, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import List, Dict

router = APIRouter(tags=["Access"])  # <--- **sem prefixo aqui**
templates = Jinja2Templates(directory="src/templates")

resources_db: List[Dict] = []

@router.get("/")
def list_resources(request: Request):
    return templates.TemplateResponse("access.html", {"request": request, "resources": resources_db})

@router.post("/add")
def add_resource(description: str = Form(...)):
    new_id = len(resources_db) + 1
    resources_db.append({"id": new_id, "description": description})
    return RedirectResponse(url="/access/", status_code=302)

@router.post("/delete")
def delete_resource(resource_id: int = Form(...)):
    global resources_db
    resources_db = [r for r in resources_db if r["id"] != resource_id]
    return RedirectResponse(url="/access/", status_code=302)

@router.get("/edit")
def edit_resource_get(request: Request, resource_id: int):
    res = next((r for r in resources_db if r["id"] == resource_id), None)
    if not res:
        return RedirectResponse(url="/access/")
    return templates.TemplateResponse("edit_access.html", {"request": request, "resource": res})

@router.post("/edit")
def edit_resource_post(resource_id: int = Form(...), description: str = Form(...)):
    for r in resources_db:
        if r["id"] == resource_id:
            r["description"] = description
            break
    return RedirectResponse(url="/access/", status_code=302)
