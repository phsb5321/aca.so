# tests/test_books_services/test_get_book_by_id_service.py
import pytest
from contextlib import asynccontextmanager
from app.database.gremlin import GraphDB
from app.database.models import BookCreate, PersonCreate
from app.services import (
    CreateBookService,
    CreatePersonService,
    GetBookByIdService,
)


@asynccontextmanager
async def generate_services():
    graph_database = GraphDB()
    create_book = CreateBookService(graph_database)
    create_person = CreatePersonService(graph_database)
    get_book_by_id = GetBookByIdService(graph_database)
    try:
        yield create_book, create_person, get_book_by_id
    finally:
        await graph_database.close_connection()


@pytest.mark.asyncio
async def test_get_book_by_id():
    async with generate_services() as (create_book, create_person, get_book_by_id):
        # Create authors using CreatePersonService
        author1 = await create_person.execute(PersonCreate(name="Author1"))
        author2 = await create_person.execute(PersonCreate(name="Author2"))

        # Call the create_book method with a new BookCreate object and the created author IDs
        created_book = await create_book.execute(BookCreate(title="Title", isbn="1234567890", stock=10), [author1, author2])

        # Call the get_book_by_id method with the created book ID
        fetched_book = await get_book_by_id.execute(created_book.id)

        # Check if the returned Book object has the correct id and title
        assert fetched_book.id == created_book.id
        assert fetched_book.title == "Title"
        assert fetched_book.isbn == "1234567890"
        assert fetched_book.stock == 10
        assert isinstance(fetched_book.authors, list)

        # Check if the authors' information is correct
        author_ids = [author.id for author in fetched_book.authors]
        author_names = [author.name for author in fetched_book.authors]
        assert set(author_ids) == set([author1.id, author2.id])
        assert set(author_names) == set(["Author1", "Author2"])

        # Call the get_book_by_id method with a non-existing book ID
        non_existing_book = await get_book_by_id.execute("non-existing-id")

        # Check if the returned Book object is None
        assert non_existing_book is None
