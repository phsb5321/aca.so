# tests/test_books_services/test_create_book_service.py
import pytest
from contextlib import asynccontextmanager
from app.database.gremlin import GraphDB
from app.database.models import BookCreate, PersonCreate
from app.services import (
    CreateBookService,
    CreatePersonService,
)


@asynccontextmanager
async def generate_services():
    graph_database = GraphDB()
    create_book = CreateBookService(graph_database)
    create_person = CreatePersonService(graph_database)
    try:
        yield create_book, create_person
    finally:
        await graph_database.close_connection()


@pytest.mark.asyncio
async def test_create_book():
    async with generate_services() as (create_book, create_person):
        # Create authors using CreatePersonService
        author1 = await create_person.execute(PersonCreate(name="Author1"))
        author2 = await create_person.execute(PersonCreate(name="Author2"))

        # Call the create_book method with a new BookCreate object and the created author IDs
        created_book = await create_book.execute(BookCreate(title="Title", isbn="1234567890", stock=10), [author1, author2])

        # Check if the returned Book object has the correct id and title
        assert isinstance(created_book.id, str)
        assert created_book.title == "Title"
        assert isinstance(created_book.isbn, str)
        assert created_book.stock == 10
        assert isinstance(created_book.authors, list)
