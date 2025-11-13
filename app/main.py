from fastapi import FastAPI
from app.database import Base, engine
from app.routes import tasks
from app import auth

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Task Management API")

app.include_router(auth.router)
app.include_router(tasks.router)
