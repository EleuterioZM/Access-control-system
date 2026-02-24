from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware

# Importar routers
from src.routers import users, access, audit, roles, api
from src.database.base import Base
from src.database.session import engine

# Criar tabelas
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Access Control & Audit System")

# Session Middleware
app.add_middleware(SessionMiddleware, secret_key="super-secret-key")

# DASHBOARD (Redirect to API docs or a simple message)
@app.get("/")
def root():
    return {"message": "Access Control API is running. Visit /docs for documentation."}

# Routers
app.include_router(api.router)
app.include_router(users.router, prefix="/users")
app.include_router(access.router) # Prefix is in the router now
app.include_router(audit.router)  # Prefix is in the router now
app.include_router(roles.router)  # Prefix is in the router now
