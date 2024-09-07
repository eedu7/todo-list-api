
from fastapi import FastAPI
from . import users, todo
app = FastAPI()

app.include_router(users.router, prefix='/users', tags=['Users'])
app.include_router(todo.router, prefix="/todo", tags=["Todo List"])