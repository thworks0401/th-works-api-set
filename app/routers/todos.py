"""TODO CRUD API — インメモリストアでタスク管理"""
from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.core.auth import verify_api_key

router = APIRouter()

# インメモリ DB代わり
todos_db: dict[int, dict] = {}
_next_id: int = 1


class TodoCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, description="タスクタイトル")
    description: Optional[str] = Field(None, max_length=1000, description="詳細")
    done: bool = Field(False, description="完了フラグ")


class TodoUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    done: Optional[bool] = None


class TodoResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    done: bool
    created_at: str
    updated_at: str


@router.post("/todos", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
async def create_todo(body: TodoCreate, _=Depends(verify_api_key)):
    """TODOを新規作成する"""
    global _next_id
    now = datetime.utcnow().isoformat()
    todo = {
        "id": _next_id,
        "title": body.title,
        "description": body.description,
        "done": body.done,
        "created_at": now,
        "updated_at": now,
    }
    todos_db[_next_id] = todo
    _next_id += 1
    return todo


@router.get("/todos", response_model=list[TodoResponse])
async def list_todos(done: Optional[bool] = None, _=Depends(verify_api_key)):
    """TODO一覧を取得。doneパラメータでフィルタリング可能。"""
    items = list(todos_db.values())
    if done is not None:
        items = [t for t in items if t["done"] == done]
    return items


@router.get("/todos/{todo_id}", response_model=TodoResponse)
async def get_todo(todo_id: int, _=Depends(verify_api_key)):
    """ID指定でTODOを取得"""
    if todo_id not in todos_db:
        raise HTTPException(status_code=404, detail=f"Todo {todo_id} not found")
    return todos_db[todo_id]


@router.put("/todos/{todo_id}", response_model=TodoResponse)
async def update_todo(todo_id: int, body: TodoUpdate, _=Depends(verify_api_key)):
    """TODOを部分更新する"""
    if todo_id not in todos_db:
        raise HTTPException(status_code=404, detail=f"Todo {todo_id} not found")
    todo = todos_db[todo_id]
    if body.title is not None:
        todo["title"] = body.title
    if body.description is not None:
        todo["description"] = body.description
    if body.done is not None:
        todo["done"] = body.done
    todo["updated_at"] = datetime.utcnow().isoformat()
    return todo


@router.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(todo_id: int, _=Depends(verify_api_key)):
    """TODOを削除する"""
    if todo_id not in todos_db:
        raise HTTPException(status_code=404, detail=f"Todo {todo_id} not found")
    del todos_db[todo_id]
