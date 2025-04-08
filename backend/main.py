from fastapi import FastAPI, Depends, HTTPException, Request
from sqlalchemy.orm import Session
import models, crud, schemas
from database import engine, Base
from auth import get_db
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from auth import router as auth_router
from auth_middleware import AuthMiddleware


app = FastAPI()
app.add_middleware(AuthMiddleware)

app.include_router(auth_router)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # ou ["*"] se estiver testando
    allow_credentials=True,
    allow_methods=["*"],  # importante para aceitar OPTIONS
    allow_headers=["*"],
)
# Cria as tabelas
Base.metadata.create_all(bind=engine)

def get_current_user(request: Request):
    print("Entrou no get_current_user")
    user = getattr(request.state, "current_user", None)
    print("user", user.id)
    if user is None:
        raise HTTPException(status_code=401, detail="Usuário não autenticado")
    return user

@app.post("/todos", response_model=schemas.TodoOut)
def create_todo(todo: schemas.TodoCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    print("current_user", current_user)
    return crud.create_todo(db, todo, current_user.id)

@app.get("/todos", response_model=list[schemas.TodoOut])
def list_todos(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return crud.get_todos(db, current_user.id)

@app.get("/todos/{todo_id}", response_model=schemas.TodoOut)
def get_todo(todo_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    todo = crud.get_todo(db, todo_id, current_user.id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@app.put("/todos/{todo_id}", response_model=schemas.TodoOut)
def update(todo_id: int, todo: schemas.TodoUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    updated = crud.update_todo(db, todo_id, todo, current_user.id)
    if not updated:
        raise HTTPException(status_code=404, detail="Todo not found")
    return updated

@app.delete("/todos/{todo_id}")
def delete(todo_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    deleted = crud.delete_todo(db, todo_id, current_user.id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Todo not found")
    return {"message": "Todo deleted successfully"}
