# tests/test_authors_services/test_list_books_by_author_service.py
import pytest
from contextlib import asynccontextmanager
from app.database.gremlin import GraphDB
from app.database.models import BookCreate, PersonCreate
from app.services import (
    CreateBookService,
    CreatePersonService,
    ListBooksByAuthorService,
)
from app.services.people_services.get_person_by_id_service import GetPersonByIdService


@pytest.fixture(autouse=True)
async def clean_db():
    graph_database = GraphDB()
    g = await graph_database.get_traversal()

    # Drop all vertices in the graph to start with an empty graph
    await g.V().drop().iterate()

    # Also, drop all edges in the graph
    await g.E().drop().iterate()

    await graph_database.close_connection()


@asynccontextmanager
async def generate_services():
    graph_database = GraphDB()

    g = await graph_database.get_traversal()

    # Drop all vertices in the graph to start with an empty graph
    await g.V().drop().iterate()

    # Also, drop all edges in the graph
    await g.E().drop().iterate()

    await graph_database.close_connection()
    create_book = CreateBookService(graph_database)
    create_person = CreatePersonService(graph_database)

    get_person_by_id = GetPersonByIdService(graph_database)
    list_books_by_author = ListBooksByAuthorService(
        graph_database, get_person_by_id)
    try:
        yield create_book, create_person, list_books_by_author
    finally:
        await graph_database.close_connection()


@pytest.mark.asyncio
async def test_list_books_by_author():
    async with generate_services() as (create_book, create_person, list_books_by_author):
        # Create authors using CreatePersonService
        author1 = await create_person.execute(PersonCreate(name="Author1"))
        author2 = await create_person.execute(PersonCreate(name="Author2"))

        # Call the create_book method with a new BookCreate object and the created author IDs
        book1 = await create_book.execute(BookCreate(title="Title1", isbn="1234567890", stock=10), [author1, author2])
        book2 = await create_book.execute(BookCreate(title="Title2", isbn="1234567891", stock=0), [author1])

        # Call the list_books_by_author method with the ID of one of the authors
        books = await list_books_by_author.execute(author_id=author1.id, skip=0, limit=10)

        # Check if the returned Book objects have the correct ids, titles, and authors
        assert len(books) == 2

        for book in books:
            if book.id == book1.id:
                assert book.title == "Title1"
                assert book.isbn == "1234567890"
                assert book.stock == 10
            elif book.id == book2.id:
                assert book.title == "Title2"
                assert book.isbn == "1234567891"
                assert book.stock == 0
