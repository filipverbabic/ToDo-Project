from fastapi import APIRouter, Depends
from src.models import User
from src.services.security_service import get_current_user
from src.services.todo_service import ITodoService, get_todo_service
from src.schemas.todo_schema import TodoCreate, TodoResponse, TodoUpdate


router = APIRouter(prefix="/todos", tags=["Todos"])

@router.get("/", response_model=list[TodoResponse])
def get_all_todos(service: ITodoService = Depends(get_todo_service), current_user: User = Depends(get_current_user)):
    return service.get_all_todos(current_user.id)

@router.post("/", status_code=201, response_model=TodoResponse)
def create_todo(todo: TodoCreate, service: ITodoService = Depends(get_todo_service), current_user: User = Depends(get_current_user)):
    return service.create_todo(todo, current_user.id)

@router.patch("/{todo_id}", response_model=TodoResponse)
def update_todo(todo_id: int, todo: TodoUpdate, service: ITodoService = Depends(get_todo_service), current_user: User = Depends(get_current_user)):
    return service.update_todo(todo_id, todo, current_user.id)

@router.delete("/{todo_id}", status_code=204)
def delete_todo(todo_id: int, service: ITodoService = Depends(get_todo_service), current_user: User = Depends(get_current_user)):
    service.delete_todo(todo_id, current_user.id)
