from sqlalchemy.orm import Session
from models import Todo
from schemas import TodoCreate, TodoUpdate

def create_todo(db: Session, todo: TodoCreate, user_id: int):
    print("user_id", user_id)
    db_todo = Todo(**todo.dict(), user_id=user_id)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

def get_todos(db: Session, user_id: int):
    return db.query(Todo).filter(Todo.user_id == user_id).all()

def get_todo(db: Session, todo_id: int, user_id: int):
    return db.query(Todo).filter(Todo.id == todo_id, Todo.user_id == user_id).first()

def update_todo(db: Session, todo_id: int, todo: TodoUpdate, user_id: int):
    db_todo = get_todo(db, todo_id, user_id)
    if db_todo:
        for key, value in todo.dict().items():
            setattr(db_todo, key, value)
        db.commit()
        db.refresh(db_todo)
    return db_todo

def delete_todo(db: Session, todo_id: int, user_id: int):
    db_todo = get_todo(db, todo_id, user_id)
    if db_todo:
        db.delete(db_todo)
        db.commit()
    return db_todo

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()
