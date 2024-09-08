from fastapi import FastAPI, HTTPException, status

from database import Base, engine

from . import todo, users

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(todo.router, prefix="/todo", tags=["Todo List"])
