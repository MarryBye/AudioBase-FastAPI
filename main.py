# Файл, який об'єднує увесь проект в єдину програму FastAPI

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routes import main_router
from database import Base, engine

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
Base.metadata.create_all(bind=engine)

app.include_router(main_router)