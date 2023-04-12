# app/routes/books_routes.py
from app.database.models import (
    Book,
    BookUpdate,
    BookCreate,
    Person,
    Rating,
    RatingCreate,
    AuthorshipCreate,
    ReadCreate
)
from app.services import (
    CreateBookService,
    GetPersonService,
    CreateAuthorshipService,
    CreateReadService,
    UpdateBookService,
    DeleteBookService,
    GetBookService,
    ListBooksService,
    ListBooksByAuthorService,
    ListReadersByBookService,
    CreateRatingService,
    ListRatingsByBookService
)
from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional

router = APIRouter()


@router.post("/books/", response_model=Book)
async def create_book_route(book: BookCreate) -> Book:
    book_repository = CreateBookService()
    people_repository = GetPersonService()

    # For each author id, confirm the person exists in the database
    for author_id in book.authors:
        author = await people_repository.execute(author_id)
        if not author:
            raise HTTPException(status_code=404, detail="Author not found")

    response = await book_repository.execute(book)
    return response


@router.post("/authorships/", response_model=None)
async def create_authorship_route(authorship: AuthorshipCreate) -> None:
    book_repository = CreateAuthorshipService()
    await book_repository.execute(authorship)


@router.put("/books/{book_id}", response_model=Book)
async def update_book_route(book_id: int, book: BookUpdate) -> Book:
    book_repository = UpdateBookService()
    db_book = await book_repository.execute(book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    response = await book_repository.execute(book_id, book)
    return response


@router.delete("/books/{book_id}")
async def delete_book_route(book_id: int) -> None:
    book_repository = DeleteBookService()
    db_book = await book_repository.execute(book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    await book_repository.execute(book_id)


@router.get("/books/{book_id}", response_model=Book)
async def get_book_by_id_route(book_id: int) -> Book:
    book_repository = GetBookService()
    db_book = await book_repository.execute(book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book


@router.get("/books/", response_model=List[Book])
async def list_books_route(skip: int = 0, limit: int = 10, in_stock: Optional[bool] = None) -> List[Book]:
    book_repository = ListBooksService()
    response = await book_repository.execute(skip=skip, limit=limit, in_stock=in_stock)
    return response


@router.get("/authors/{author_id}/books", response_model=List[Book])
async def list_books_by_author_route(author_id: int, skip: int = 0, limit: int = 10) -> List[Book]:
    book_repository = ListBooksByAuthorService()
    response = await book_repository.execute(author_id, skip=skip, limit=limit)
    return response


@router.get("/books/{book_id}/readers", response_model=List[Person])
async def list_readers_by_book_route(book_id: int, skip: int = 0, limit: int = 10) -> List[Person]:
    book_repository = ListReadersByBookService()
    response = await book_repository.execute(book_id, skip=skip, limit=limit)
    return response


@router.get("/books/{book_id}/ratings", response_model=List[Rating])
async def list_ratings_by_book_route(book_id: int, skip: int = 0, limit: int = 10) -> List[Rating]:
    book_repository = ListRatingsByBookService()
    response = await book_repository.execute(book_id, skip=skip, limit=limit)
    return response


@router.post("/ratings/", response_model=Rating)
async def create_rating_route(rating: RatingCreate) -> Rating:
    book_repository = CreateRatingService()
    response = await book_repository.execute(rating)
    return response


@router.post("/reads/", response_model=None)
async def create_read_route(read: ReadCreate) -> None:
    book_repository = CreateReadService()
    await book_repository.execute(read)
