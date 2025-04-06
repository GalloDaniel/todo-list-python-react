import os
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from dotenv import load_dotenv
import psycopg2
from urllib.parse import urlparse

load_dotenv()
DATABASE_URL = os.environ.get("DATABASE_URL")

# Extrair nome do banco de dados e montar uma URL sem ele
parsed_url = urlparse(DATABASE_URL)
db_name = parsed_url.path[1:]  # remove o `/` do começo
default_database_url = DATABASE_URL.replace(f"/{db_name}", "/postgres")

# Conecta no banco 'postgres' para criar o banco principal se não existir
try:
    default_engine = create_engine(default_database_url, isolation_level="AUTOCOMMIT")
    with default_engine.connect() as conn:
        result = conn.execute(
            text("SELECT 1 FROM pg_database WHERE datname = :name"),
            {"name": db_name}
        )
        if not result.fetchone():
            conn.execute(text(f'CREATE DATABASE "{db_name}"'))
        else:
            print(f"Banco de dados '{db_name}' já existe.")
except OperationalError as e:
    print("Erro ao conectar para criar o banco:", e)
    raise

# Agora conecta normalmente no banco que você quer usar
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
