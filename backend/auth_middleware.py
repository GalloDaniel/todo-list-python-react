from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from fastapi import Request
from auth_token import verify_token

# Chave secreta usada para assinar os tokens (mesma usada na criação)
SECRET_KEY = "sua_chave_secreta"
ALGORITHM = "HS256"  # ou o que você estiver usando

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Pula verificação em rotas públicas
        if request.url.path in ["/login", "/docs", "/openapi.json"]:
            return await call_next(request)

        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Basic "):
            return JSONResponse(status_code=401, content={"detail": "Token de autenticação ausente"})

        token = auth_header.split(" ")[1]

        try:
            payload = verify_token(token)

            if payload is None:
                return JSONResponse(status_code=401, content={"detail": "Token inválido"})
        except:
            return JSONResponse(status_code=401, content={"detail": "Token expirado"})

        return await call_next(request)
