# app/readers_routes.py
from app.database.models import (
    Person,
    Rating,
    RatingCreate,
    ReadCreate
)
from app.services import (
    CreateReadService,
    ListReadersByBookService,
    CreateRatingService,
    ListRatingsByBookService
)
from fastapi import APIRouter
from app.database.gremlin import GraphDB
from typing import List

router = APIRouter()


@router.get("/{book_id}", response_model=List[Person])
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
