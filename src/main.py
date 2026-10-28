from fastapi import FastAPI
from src.database import engine, Base
from src.routers import auth_router, todo_router, user_router

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(todo_router.router)
app.include_router(user_router.router)
app.include_router(auth_router.router)


@app.get("/")
def root():
    return {"message": "TODO is running!"}


