# main.py
from fastapi import FastAPI, HTTPException
from typing import List, Optional
from database import GraphDB

from models import PersonCreate, PersonUpdate, BookCreate, BookUpdate, RatingCreate, Person, Book, Rating
from usecases.usecases import (create_person, update_person, delete_person, get_person, get_persons, create_book, update_book,
                               delete_book, get_book, get_books, get_books_by_author, get_readers_by_book, get_ratings_by_book,
                               create_rating)

app = FastAPI()


@app.post("/persons/", response_model=Person)
async def create_person_route(person: PersonCreate) -> Person:
    # Use the create_person_async function instead of the create_person function
    return await create_person(GraphDB(), person)


@app.put("/persons/{person_id}", response_model=Person)
async def update_person_route(person_id: int, person: PersonUpdate) -> Person:
    db_person = get_person(person_id)
    if not db_person:
        raise HTTPException(status_code=404, detail="Person not found")
    return update_person(person_id, person)


@app.delete("/persons/{person_id}")
async def delete_person_route(person_id: int) -> None:
    db_person = get_person(person_id)
    if not db_person:
        raise HTTPException(status_code=404, detail="Person not found")
    delete_person(person_id)


@app.get("/persons/{person_id}", response_model=Person)
async def get_person_route(person_id: int) -> Person:
    db_person = get_person(person_id)
    if not db_person:
        raise HTTPException(status_code=404, detail="Person not found")
    return db_person


@app.get("/persons/", response_model=List[Person])
async def get_persons_route(skip: int = 0, limit: int = 10) -> List[Person]:
    return get_persons(skip=skip, limit=limit)

# CRUD for Book


@app.post("/books/", response_model=Book)
async def create_book_route(book: BookCreate) -> Book:
    return create_book(book)


@app.put("/books/{book_id}", response_model=Book)
async def update_book_route(book_id: int, book: BookUpdate) -> Book:
    db_book = get_book(book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return update_book(book_id, book)


@app.delete("/books/{book_id}")
async def delete_book_route(book_id: int) -> None:
    db_book = get_book(book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    delete_book(book_id)


@app.get("/books/{book_id}", response_model=Book)
async def get_book_route(book_id: int) -> Book:
    db_book = get_book(book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book


@app.get("/books/", response_model=List[Book])
async def get_books_route(skip: int = 0, limit: int = 10, in_stock: Optional[bool] = None) -> List[Book]:
    return get_books(skip=skip, limit=limit, in_stock=in_stock)


@app.get("/authors/{author_id}/books", response_model=List[Book])
async def get_books_by_author_route(author_id: int, skip: int = 0, limit: int = 10) -> List[Book]:
    return get_books_by_author(author_id, skip=skip, limit=limit)


@app.get("/books/{book_id}/readers", response_model=List[Person])
async def get_readers_by_book_route(book_id: int, skip: int = 0, limit: int = 10) -> List[Person]:
    return get_readers_by_book(book_id, skip=skip, limit=limit)


@app.get("/books/{book_id}/ratings", response_model=List[Rating])
async def get_ratings_by_book_route(book_id: int, skip: int = 0, limit: int = 10) -> List[Rating]:
    return get_ratings_by_book(book_id, skip=skip, limit=limit)


@app.post("/ratings/", response_model=Rating)
async def create_rating_route(rating: RatingCreate) -> Rating:
    return create_rating(rating)
