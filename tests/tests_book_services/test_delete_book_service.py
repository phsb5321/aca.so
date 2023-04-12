# tests/test_books_services/test_delete_book_service.py
import pytest
from contextlib import asynccontextmanager
from app.database.gremlin import GraphDB
from app.database.models import BookCreate, PersonCreate
from app.services import (
    CreateBookService,
    CreatePersonService,
    DeleteBookService,
)


@asynccontextmanager
async def generate_services():
    graph_database = GraphDB()
    create_book = CreateBookService(graph_database)
    create_person = CreatePersonService(graph_database)
    delete_book = DeleteBookService(graph_database)
    try:
        yield create_book, create_person, delete_book
    finally:
        await graph_database.close_connection()


@pytest.mark.asyncio
async def test_delete_book():
    async with generate_services() as (create_book, create_person, delete_book):
        # Create authors using CreatePersonService
        author1 = await create_person.execute(PersonCreate(name="Author1"))
        author2 = await create_person.execute(PersonCreate(name="Author2"))

        # Call the create_book method with a new BookCreate object and the created author IDs
        created_book = await create_book.execute(BookCreate(title="Title", isbn="1234567890", stock=10), [author1, author2])

        # Call the delete_book method with the created book ID
        deleted_book_id = await delete_book.execute(created_book.id)

        # Check if the returned book ID is correct
        assert deleted_book_id == created_book.id
