from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict

router = APIRouter(prefix="/access", tags=["Access"])

# Mock resources for now, should be migrated to models if needed
resources_db: List[Dict] = []

@router.get("/")
def list_resources():
    return resources_db

@router.post("/add")
def add_resource(description: str):
    new_id = len(resources_db) + 1
    new_res = {"id": new_id, "description": description}
    resources_db.append(new_res)
    return new_res

@router.delete("/{resource_id}")
def delete_resource(resource_id: int):
    global resources_db
    resources_db = [r for r in resources_db if r["id"] != resource_id]
    return {"message": "Resource deleted"}
