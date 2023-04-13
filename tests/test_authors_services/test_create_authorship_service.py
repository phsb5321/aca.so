# tests/test_books_services/test_create_authorship_service.py
import pytest
from contextlib import asynccontextmanager
from app.database.gremlin import GraphDB
from app.database.models import AuthorshipCreate, PersonCreate, BookCreate
from app.services import CreateAuthorshipService, CreateBookService, CreatePersonService, GetBookByIdService, GetPersonByIdService


# Fixture to share an instance of services between tests and clean up the connection after all tests are run
@asynccontextmanager
async def generate_services():
    graph_database = GraphDB()
    create_person = CreatePersonService(graph_database)
    create_book = CreateBookService(graph_database)

    get_book_by_id = GetBookByIdService(graph_database)
    get_person_by_id = GetPersonByIdService(graph_database)

    create_authorship = CreateAuthorshipService(
        graph_database, get_book_by_id, get_person_by_id)
    try:
        yield create_person, create_book, create_authorship
    finally:
        await graph_database.close_connection()


# Test the execute method in CreateAuthorshipService
@pytest.mark.asyncio
async def test_create_authorship():
    async with generate_services() as (create_person, create_book, create_authorship):
        # Create a new person
        person = await create_person.execute(PersonCreate(name="John Doe"))

        # Create a new book
        book = await create_book.execute(BookCreate(title="Title", isbn="1234567890", stock=10), [person])

        # Create a new authorship between the person and the book
        authorship = await create_authorship.execute(AuthorshipCreate(author_id=person.id, book_id=book.id))

        # Check if the authorship was created successfully
        assert authorship.author.id == person.id
        assert authorship.book.id == book.id
