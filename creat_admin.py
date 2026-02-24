# create_admin.py
from src.database.session import SessionLocal, engine
from src.database.base import Base
from src.models.user import User  # ajuste para o caminho do seu modelo de usuário
from passlib.context import CryptContext

# Configuração de hash de senha (usando pbkdf2_sha256)
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def create_admin():
    # Garantir que as tabelas existem
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # Verifica se já existe um admin
    admin = db.query(User).filter(User.username == "admin").first()
    if admin:
        print("Admin já existe!")
        db.close()
        return

    novo_admin = User(
        username="admin",
        email="admin@teste.com",
        password=hash_password("1234"),  # senha do admin
        role="admin",
        is_active=True,
        is_superuser=True
    )

    db.add(novo_admin)
    db.commit()
    db.close()
    print("Admin criado com sucesso! Usuário: admin | Senha: 1234")

if __name__ == "__main__":
    create_admin()
