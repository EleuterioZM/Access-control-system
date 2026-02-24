from fastapi import FastAPI, Request, Cookie
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware

# Importar routers
from src.routers import auth, users, access, audit, roles, api
from src.database.base import Base
from src.database.session import engine

# Criar tabelas
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Access Control & Audit System")

# Templates e static
templates = Jinja2Templates(directory="src/templates")
app.mount("/static", StaticFiles(directory="src/static"), name="static")

# Session Middleware
app.add_middleware(SessionMiddleware, secret_key="super-secret-key")

# DASHBOARD
@app.get("/", response_class=RedirectResponse)
def root():
    return RedirectResponse(url="/dashboard")

@app.get("/dashboard")
def dashboard(request: Request, user: str | None = Cookie(default=None)):
    if not user:
        return RedirectResponse(url="/auth/login")
    return templates.TemplateResponse(
        "dashboard.html", {"request": request, "user": user}
    )

# Routers
app.include_router(auth.router, prefix="/auth")
app.include_router(users.router, prefix="/users")
app.include_router(access.router, prefix="/access")
app.include_router(audit.router, prefix="/audit")
app.include_router(roles.router)  # já tem prefix="/roles" dentro do router
