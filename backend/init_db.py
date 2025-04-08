from database import Base, engine
from models import User, Todo

print("Criando as tabelas no banco de dados...")
Base.metadata.create_all(bind=engine)
