from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from fastapi import Request
from auth_token import verify_token
from sqlalchemy.orm import Session
from database import SessionLocal
import models

# Chave secreta usada para assinar os tokens (mesma usada na criação)
SECRET_KEY = "sua_chave_secreta"
ALGORITHM = "HS256"  # ou o que você estiver usando

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path in ["/login", "/docs", "/openapi.json"]:
            return await call_next(request)

        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Basic "):
            return JSONResponse(status_code=401, content={"detail": "Token de autenticação ausente ou inválido"})

        token = auth_header.split(" ")[1]
        payload = verify_token(token)

        if payload is None:
            return JSONResponse(status_code=401, content={"detail": "Token inválido ou expirado"})

        user_id = payload.get("sub")
        if user_id is None:
            return JSONResponse(status_code=401, content={"detail": "Token sem ID de usuário"})

        # Cria uma sessão do banco manualmente aqui (porque estamos fora do contexto FastAPI)
        db: Session = SessionLocal()
        user = db.query(models.User).filter(models.User.id == user_id).first()
        db.close()

        if not user:
            return JSONResponse(status_code=401, content={"detail": "Usuário não encontrado"})

        # Armazena o usuário na request
        request.state.current_user = user

        return await call_next(request)
