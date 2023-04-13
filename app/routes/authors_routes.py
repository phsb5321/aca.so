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

from app.services import GetPersonByIdService
from app.services.books_services.get_book_by_id_service import GetBookByIdService

router = APIRouter()


@router.get("/{author_id}/books", response_model=List[Book])
async def list_books_by_author_route(author_id: str, skip: int = 0, limit: int = 10) -> List[Book]:
    graph_database = GraphDB()
    get_person_by_id = GetPersonByIdService(graph_database)
    book_repository = ListBooksByAuthorService(
        graph_database, get_person_by_id)
    response = await book_repository.execute(author_id, skip=skip, limit=limit)
    return response


@router.post("/authorships", response_model=None)
async def create_authorship_route(authorship: AuthorshipCreate) -> None:
    graph_database = GraphDB()
    get_book_by_id = GetBookByIdService(graph_database)
    get_person_by_id = GetPersonByIdService(graph_database)
    book_repository = CreateAuthorshipService(
        graph_database, get_book_by_id, get_person_by_id)
    await book_repository.execute(authorship)
