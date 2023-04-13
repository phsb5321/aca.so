# app/authors_routes.py
from app.database.models import (
    Book,
    AuthorshipCreate
)
from app.services import (
    CreateAuthorshipService,
    ListBooksByAuthorService
)
from fastapi import APIRouter
from app.database.gremlin import GraphDB
from typing import List

router = APIRouter()


@router.get("/authors/{author_id}/books", response_model=List[Book])
async def list_books_by_author_route(author_id: int, skip: int = 0, limit: int = 10) -> List[Book]:
    graph_database = GraphDB()
    book_repository = ListBooksByAuthorService(graph_database)
    response = await book_repository.execute(author_id, skip=skip, limit=limit)
    return response


@router.post("/authorships", response_model=None)
async def create_authorship_route(authorship: AuthorshipCreate) -> None:
    graph_database = GraphDB()
    book_repository = CreateAuthorshipService(graph_database)
    await book_repository.execute(authorship)
