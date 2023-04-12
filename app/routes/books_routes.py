# app/routes_routes.py
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
    GetPersonByIdService,
    CreateAuthorshipService,
    CreateReadService,
    UpdateBookService,
    DeleteBookService,
    GetBookByIdService,
    ListBooksService,
    ListBooksByAuthorService,
    ListReadersByBookService,
    CreateRatingService,
    ListRatingsByBookService
)
from fastapi import APIRouter, Depends, HTTPException
from app.database.gremlin import GraphDB
from typing import List, Optional

router = APIRouter()


@router.post("", response_model=Book)
async def create_book_route(book: BookCreate) -> Book:
    graph_database = GraphDB()
    create_book = CreateBookService(graph_database)
    get_person_by_id = GetPersonByIdService(graph_database)

    # For each author id, confirm the person exists in the database
    validated_authors = []
    for author_id in book.author_ids:
        author = await get_person_by_id.execute(author_id)
        if not author:
            raise HTTPException(status_code=404, detail="Author not found")
        validated_authors.append(author)

    response = await create_book.execute(book, validated_authors)
    return response


@router.put("/{book_id}", response_model=Book)
async def update_book_route(book_id: str, book: BookUpdate) -> Book:
    graph_database = GraphDB()
    book_repository = UpdateBookService(graph_database)
    db_book = await book_repository.execute(book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    response = await book_repository.execute(book_id, book)
    return response


@router.delete("/{book_id}")
async def delete_book_route(book_id: str) -> None:
    graph_database = GraphDB()
    book_repository = DeleteBookService(graph_database)
    db_book = await book_repository.execute(book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    await book_repository.execute(book_id)


@router.get("/{book_id}", response_model=Book)
async def get_book_by_id_route(book_id: str) -> Book:
    graph_database = GraphDB()
    book_repository = GetBookByIdService(graph_database)
    db_book = await book_repository.execute(book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book


@router.get("", response_model=List[Book])
async def list_books_route(skip: int = 0, limit: int = 10, in_stock: Optional[bool] = None) -> List[Book]:
    graph_database = GraphDB()
    book_repository = ListBooksService(graph_database)
    response = await book_repository.execute(skip=skip, limit=limit, in_stock=in_stock)
    return response


@router.get("/authors/{author_id}", response_model=List[Book])
async def list_books_by_author_route(author_id: int, skip: int = 0, limit: int = 10) -> List[Book]:
    graph_database = GraphDB()
    book_repository = ListBooksByAuthorService(graph_database)
    response = await book_repository.execute(author_id, skip=skip, limit=limit)
    return response


@router.get("/{book_id}/readers", response_model=List[Person])
async def list_readers_by_book_route(book_id: str, skip: int = 0, limit: int = 10) -> List[Person]:
    graph_database = GraphDB()
    book_repository = ListReadersByBookService(graph_database)
    response = await book_repository.execute(book_id, skip=skip, limit=limit)
    return response


@router.get("/{book_id}/ratings", response_model=List[Rating])
async def list_ratings_by_book_route(book_id: str, skip: int = 0, limit: int = 10) -> List[Rating]:
    graph_database = GraphDB()
    book_repository = ListRatingsByBookService(graph_database)
    response = await book_repository.execute(book_id, skip=skip, limit=limit)
    return response


@router.post("/ratings", response_model=Rating)
async def create_rating_route(rating: RatingCreate) -> Rating:
    graph_database = GraphDB()
    book_repository = CreateRatingService(graph_database)
    response = await book_repository.execute(rating)
    return response


@router.post("/reads", response_model=None)
async def create_read_route(read: ReadCreate) -> None:
    graph_database = GraphDB()
    book_repository = CreateReadService(graph_database)
    await book_repository.execute(read)


@router.post("/authorships", response_model=None)
async def create_authorship_route(authorship: AuthorshipCreate) -> None:
    graph_database = GraphDB()
    book_repository = CreateAuthorshipService(graph_database)
    await book_repository.execute(authorship)
