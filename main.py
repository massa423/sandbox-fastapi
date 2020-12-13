from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session, sessionmaker
from starlette.requests import Request
from starlette.responses import Response
from starlette.middleware.base import RequestResponseEndpoint
from pydantic import BaseModel
from db import Todo, engine
from typing import List, Dict

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class TodoIn(BaseModel):
    """
    TodoIn
    """

    title: str
    done: bool


def get_todo(db_session: Session, todo_id: int) -> Todo:
    """
    get_todo
    """
    return db_session.query(Todo).filter(Todo.id == todo_id).first()


def get_db(request: Request) -> Session:
    """
    get_db
    """
    return request.state.db


app = FastAPI()


@app.get("/todos/")
def read_todos(db: Session = Depends(get_db)) -> List:
    """
    read_todos
    """
    todos = db.query(Todo).all()
    return todos


@app.get("/todos/{todo_id}")
def read_todo(todo_id: int, db: Session = Depends(get_db)) -> Dict:
    """
    read_todo
    """
    todo = get_todo(db, todo_id)
    return todo


@app.post("/todos/")
async def create_todo(todo_in: TodoIn, db: Session = Depends(get_db)) -> Dict:
    todo = Todo(title=todo_in.title, done=False)
    db.add(todo)
    db.commit()
    todo = get_todo(db, todo.id)
    return todo


@app.put("/todos/{todo_id}")
async def update_todo(
    todo_id: int, todo_in: TodoIn, db: Session = Depends(get_db)
) -> Dict:
    todo = get_todo(db, todo_id)
    todo.title = todo_in.title
    todo.done = todo_in.done
    db.commit()
    todo = get_todo(db, todo_id)
    return todo


@app.delete("/todos/{todo_id}")
async def delete_todo(todo_id: int, db: Session = Depends(get_db)) -> None:
    todo = get_todo(db, todo_id)
    db.delete(todo)
    db.commit()


@app.middleware("http")
async def db_session_middleware(
    request: Request, call_next: RequestResponseEndpoint
) -> Response:
    request.state.db = SessionLocal()
    response = await call_next(request)
    request.state.db.close()
    return response
