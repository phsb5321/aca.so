# tests/test_books_services/test_update_book_service.py
import pytest
from contextlib import asynccontextmanager
from app.database.gremlin import GraphDB
from app.database.models import BookCreate, BookUpdate, PersonCreate
from app.services import (
    CreateBookService,
    CreatePersonService,
    UpdateBookService,
)


@asynccontextmanager
async def generate_services():
    graph_database = GraphDB()
    create_book = CreateBookService(graph_database)
    create_person = CreatePersonService(graph_database)
    update_book = UpdateBookService(graph_database)
    try:
        yield create_book, create_person, update_book
    finally:
        await graph_database.close_connection()


@pytest.mark.asyncio
async def test_update_book():
    async with generate_services() as (create_book, create_person, update_book):
        # Create authors using CreatePersonService
        author1 = await create_person.execute(PersonCreate(name="Author1"))
        author2 = await create_person.execute(PersonCreate(name="Author2"))

        # Create a new book using CreateBookService
        created_book = await create_book.execute(BookCreate(title="Title", isbn="1234567890", stock=10), [author1, author2])

        # Update the created book using UpdateBookService
        updated_book = await update_book.execute(created_book.id, BookUpdate(title="New Title", isbn="0987654321", stock=20))

        # Check if the returned Book object has the correct id, title, isbn, and stock
        assert updated_book.id == created_book.id
        assert updated_book.title == "New Title"
        assert updated_book.isbn == "0987654321"
        assert updated_book.stock == 20
