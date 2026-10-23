from fastapi import FastAPI
from src.database import engine, Base
from src.routers import todo_router

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(todo_router.router)

@app.get("/")
def root():
    return {"message": "TODO is running!"}


