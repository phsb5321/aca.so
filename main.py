# main.py
from fastapi import FastAPI
from app.routes import people_routes, books_routes, authors_routes, readers_routes

app = FastAPI()

app.include_router(people_routes.router, prefix="/people", tags=["people"])
app.include_router(books_routes.router, prefix="/books", tags=["books"])
app.include_router(authors_routes.router, prefix="/authors", tags=["authors"])
app.include_router(readers_routes.router, prefix="/readers", tags=["readers"])
