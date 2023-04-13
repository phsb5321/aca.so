# tests/test_readers_services/test_list_readers_by_book_service.py
import pytest
from contextlib import asynccontextmanager
from app.database.gremlin import GraphDB
from app.database.models import PersonCreate, BookCreate, ReadCreate
from app.services import (
    CreatePersonService,
    CreateBookService,
    CreateReadService,
    GetPersonByIdService,
    GetBookByIdService,
    ListReadersByBookService
)


@asynccontextmanager
async def generate_services():
    graph_database = GraphDB()
    create_person = CreatePersonService(graph_database)
    create_book = CreateBookService(graph_database)

    get_person_by_id = GetPersonByIdService(graph_database)
    get_book_by_id = GetBookByIdService(graph_database)

    create_read = CreateReadService(
        graph_database,
        get_person_by_id,
        get_book_by_id
    )

    list_readers_by_book = ListReadersByBookService(
        graph_database, get_person_by_id)

    try:
        yield create_person, create_book, create_read, list_readers_by_book
    finally:
        await graph_database.close_connection()


@pytest.mark.asyncio
async def test_list_readers_by_book_service():
    async with generate_services() as (create_person, create_book, create_read, list_readers_by_book):

        # Create a new person (reader)
        reader = await create_person.execute(PersonCreate(name="John Doe"))

        # Create a new person (author)
        author = await create_person.execute(PersonCreate(name="Jane Smith"))

        # Create a new book by the author
        book = await create_book.execute(BookCreate(title="Title", isbn="1234567890", stock=10), [author])

        # Create a new read for the book by the reader
        await create_read.execute(ReadCreate(reader_id=reader.id, book_id=book.id))

        # Call the list_readers_by_book method
        readers = await list_readers_by_book.execute(book_id=book.id, skip=0, limit=10)

        # Check if the returned Person object has the correct id and name
        assert len(readers) == 1
        assert readers[0].id == reader.id
        assert readers[0].name == "John Doe"
