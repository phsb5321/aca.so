# tests/test_readers_services/test_create_read_service.py

import pytest
from contextlib import asynccontextmanager
from app.database.models import PersonCreate, BookCreate, ReadCreate
from app.database.gremlin import GraphDB
from app.services import (
    CreatePersonService,
    CreateBookService,
    CreateReadService,
    GetPersonByIdService,
    GetBookByIdService
)


@asynccontextmanager
async def generate_services():
    graph_database = GraphDB()
    create_person = CreatePersonService(graph_database)
    create_book = CreateBookService(graph_database)
    get_person_by_id = GetPersonByIdService(graph_database)
    get_book_by_id = GetBookByIdService(graph_database)
    create_read = CreateReadService(
        graph_database, get_person_by_id, get_book_by_id)

    try:
        yield create_person, create_book, create_read
    finally:
        await graph_database.close_connection()


@pytest.mark.asyncio
async def test_create_read():
    async with generate_services() as (create_person, create_book, create_read):

        # Create a new person (reader)s
        reader = await create_person.execute(PersonCreate(name="John Doe"))

        # Create a new person (author)
        author = await create_person.execute(PersonCreate(name="Jane Smith"))

        # Create a new book by the author
        book = await create_book.execute(BookCreate(title="Title", isbn="1234567890", stock=10), [author])

        # Create a new read for the book by the reader
        read = await create_read.execute(ReadCreate(reader_id=reader.id, book_id=book.id))

        # Check if the read was created successfully
        assert read.reader.id == reader.id
        assert read.reader.name == "John Doe"
        assert read.book.id == book.id
        assert read.book.title == "Title"
