# tests/test_readers_services/test_list_ratings_by_book_service.py

from fastapi import HTTPException
import pytest
from contextlib import asynccontextmanager
from app.database.gremlin import GraphDB
from app.database.models import PersonCreate, BookCreate, ReadCreate, RatingCreate
from app.services import (
    CreatePersonService,
    CreateBookService,
    CreateReadService,
    CreateRatingService,
    GetPersonByIdService,
    GetBookByIdService,
    ListReadersByBookService,
    ListRatingsByBookService,
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

    create_rating = CreateRatingService(
        graph_database,
        get_person_by_id,
        get_book_by_id
    )

    list_ratings_by_book = ListRatingsByBookService(
        graph_database,  get_book_by_id, get_person_by_id)

    try:
        yield create_person, create_book, create_read, create_rating, list_ratings_by_book
    finally:
        await graph_database.close_connection()


@pytest.mark.asyncio
async def test_list_ratings_by_book_service():
    async with generate_services() as (create_person, create_book, create_read, create_rating,  list_ratings_by_book):

        # Create a new person (reader)
        reader = await create_person.execute(PersonCreate(name="John Doe"))

        # Create a new person (author)
        author = await create_person.execute(PersonCreate(name="Jane Smith"))

        # Create a new book by the author
        book = await create_book.execute(BookCreate(title="Title", isbn="1234567890", stock=10), [author])

        # Create a new read for the book by the reader
        await create_read.execute(ReadCreate(reader_id=reader.id, book_id=book.id))

        # Create a new rating for the book by the reader
        await create_rating.execute(RatingCreate(reader_id=reader.id, book_id=book.id, score=3, comment="Good book"))

        # Call the list_ratings_by_book method
        ratings = await list_ratings_by_book.execute(book_id=book.id, skip=0, limit=10)

        # Check if the returned Rating object has the correct attributes
        assert len(ratings) == 1
        assert ratings[0].score == 3
        assert ratings[0].comment == "Good book"
        assert ratings[0].book.id == book.id
        assert ratings[0].book.title == "Title"

        # Call the list_ratings_by_book method with invalid book ID
        with pytest.raises(HTTPException):
            await list_ratings_by_book.execute(book_id=-1, skip=0, limit=10)

        # Call the list_ratings_by_book method with non-existent book ID
        with pytest.raises(HTTPException):
            await list_ratings_by_book.execute(book_id=99999, skip=0, limit=10)
