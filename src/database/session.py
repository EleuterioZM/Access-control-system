import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Se não houver DATABASE_URL, usa SQLite como fallback local
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")

# O SQLite precisa do connect_args, o PostgreSQL não.
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    # Ajuste para render que às vezes manda postgres:// em vez de postgresql://
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
