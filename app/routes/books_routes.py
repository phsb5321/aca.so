from fastapi import APIRouter, HTTPException
from typing import List, Optional
from app.database.models import Book, BookUpdate, BookCreate, Person, Rating, RatingCreate
from fastapi import APIRouter, Depends, HTTPException
from app.services.books_services import BookUseCases

router = APIRouter()


@router.post("/books/", response_model=Book)
async def create_book_route(book: BookCreate) -> Book:
    book_repository = BookUseCases()
    response = await book_repository.create_book(book)
    return response


@router.put("/books/{book_id}", response_model=Book)
async def update_book_route(book_id: int, book: BookUpdate) -> Book:
    book_repository = BookUseCases()
    db_book = await book_repository.get_book(book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    response = await book_repository.update_book(book_id, book)
    return response


@router.delete("/books/{book_id}")
async def delete_book_route(book_id: int) -> None:
    book_repository = BookUseCases()
    db_book = await book_repository.get_book(book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    await book_repository.delete_book(book_id)


@router.get("/books/{book_id}", response_model=Book)
async def get_book_route(book_id: int) -> Book:
    book_repository = BookUseCases()
    db_book = await book_repository.get_book(book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book


@router.get("/books/", response_model=List[Book])
async def get_books_route(skip: int = 0, limit: int = 10, in_stock: Optional[bool] = None) -> List[Book]:
    book_repository = BookUseCases()
    response = await book_repository.get_books(skip=skip, limit=limit, in_stock=in_stock)
    return response


@router.get("/authors/{author_id}/books", response_model=List[Book])
async def get_books_by_author_route(author_id: int, skip: int = 0, limit: int = 10) -> List[Book]:
    book_repository = BookUseCases()
    response = await book_repository.get_books_by_author(author_id, skip=skip, limit=limit)
    return response


@router.get("/books/{book_id}/readers", response_model=List[Person])
async def get_readers_by_book_route(book_id: int, skip: int = 0, limit: int = 10) -> List[Person]:
    book_repository = BookUseCases()
    response = await book_repository.get_readers_by_book(book_id, skip=skip, limit=limit)
    return response


@router.get("/books/{book_id}/ratings", response_model=List[Rating])
async def get_ratings_by_book_route(book_id: int, skip: int = 0, limit: int = 10) -> List[Rating]:
    book_repository = BookUseCases()
    response = await book_repository.get_ratings_by_book(book_id, skip=skip, limit=limit)
    return response


@router.post("/ratings/", response_model=Rating)
async def create_rating_route(rating: RatingCreate) -> Rating:
    book_repository = BookUseCases()
    response = await book_repository.create_rating(rating)
    return response
