# tests/test_readers_services/test_create_rating_service.py

import pytest
from contextlib import asynccontextmanager
from app.database.models import PersonCreate, BookCreate, RatingCreate
from app.database.gremlin import GraphDB
from app.services.people_services.create_person_service import CreatePersonService
from app.services.books_services.create_book_service import CreateBookService
from app.services.readers_services.create_rating_service import CreateRatingService
from app.services.people_services.get_person_by_id_service import GetPersonByIdService
from app.services.books_services.get_book_by_id_service import GetBookByIdService


@asynccontextmanager
async def generate_services():
    graph_database = GraphDB()
    create_person = CreatePersonService(graph_database)
    create_book = CreateBookService(graph_database)
    get_person_by_id = GetPersonByIdService(graph_database)
    get_book_by_id = GetBookByIdService(graph_database)
    create_rating = CreateRatingService(
        graph_database, get_person_by_id, get_book_by_id)

    try:
        yield create_person, create_book, create_rating
    finally:
        await graph_database.close_connection()


@pytest.mark.asyncio
async def test_create_rating():
    async with generate_services() as (create_person, create_book, create_rating):

        # Create a new person (reader)s
        reader = await create_person.execute(PersonCreate(name="John Doe"))

        # Create a new person (author)
        author = await create_person.execute(PersonCreate(name="Jane Smith"))

        # Create a new book by the author
        book = await create_book.execute(BookCreate(title="Title", isbn="1234567890", stock=10), [author])

        # Create a new rating for the book by the reader
        rating = await create_rating.execute(RatingCreate(reader_id=reader.id, book_id=book.id, score=4, comment="Good book"))

        # Check if the rating was created successfully
        assert rating.reader.id == reader.id
        assert rating.reader.name == "John Doe"
        assert rating.book.id == book.id
        assert rating.book.title == "Title"
        assert rating.score == 4
        assert rating.comment == "Good book"
