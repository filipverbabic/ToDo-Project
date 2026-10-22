from fastapi import FastAPI
from src.database import engine, Base
from src import models

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def root():
    return {"message": "TODO is running!"}


