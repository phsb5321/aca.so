# main.py
from fastapi import FastAPI
from app.routes import people_routes, books_routes

app = FastAPI()

app.include_router(people_routes.router, prefix="/people", tags=["people"])
app.include_router(books_routes.router, prefix="/books", tags=["books"])
