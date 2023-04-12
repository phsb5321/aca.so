# tests/test_books_services/test_list_books_service.py
import pytest
from contextlib import asynccontextmanager
from app.database.gremlin import GraphDB
from app.database.models import BookCreate, PersonCreate
from app.services import (
    CreateBookService,
    CreatePersonService,
    ListBooksService,
)


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
    list_books = ListBooksService(graph_database)
    try:
        yield create_book, create_person, list_books
    finally:
        await graph_database.close_connection()


@pytest.mark.asyncio
async def test_list_books_service():
    async with generate_services() as (create_book, create_person, list_books):
        # Create authors using CreatePersonService
        author1 = await create_person.execute(PersonCreate(name="Author1"))
        author2 = await create_person.execute(PersonCreate(name="Author2"))

        # Call the create_book method with a new BookCreate object and the created author IDs
        book1 = await create_book.execute(BookCreate(title="Title1", isbn="1234567890", stock=10), [author1, author2])
        book2 = await create_book.execute(BookCreate(title="Title2", isbn="1234567891", stock=0), [author1])

        # Call the list_books method
        books = await list_books.execute(skip=0, limit=10)

        # Check if the returned Book objects have the correct ids, titles, and authors
        assert len(books) == 2

        for book in books:
            if book.id == book1.id:
                assert book.title == "Title1"
                assert book.isbn == "1234567890"
                assert book.stock == 10
                assert isinstance(book.authors, list)
                author_ids = [author.id for author in book.authors]
                author_names = [author.name for author in book.authors]
                assert set(author_ids) == set([author1.id, author2.id])
                assert set(author_names) == set(["Author1", "Author2"])
            elif book.id == book2.id:
                assert book.title == "Title2"
                assert book.isbn == "1234567891"
                assert book.stock == 0
                assert isinstance(book.authors, list)
                author_ids = [author.id for author in book.authors]
                author_names = [author.name for author in book.authors]
                assert set(author_ids) == set([author1.id])
                assert set(author_names) == set(["Author1"])

        # Call the list_books method filtering by books in stock
        in_stock_books = await list_books.execute(skip=0, limit=10, in_stock=True)

        # Check if the returned Book objects have the correct ids and are in stock
        assert len(in_stock_books) == 1
        assert in_stock_books[0].id == book1.id
        assert in_stock_books[0].stock == 10

        # Call the list_books method filtering by books out of stock
        out_of_stock_books = await list_books.execute(skip=0, limit=10, in_stock=False)

        # Check if the returned Book objects have the correct ids and are out of stock
        assert len(out_of_stock_books) == 1
        assert out_of_stock_books[0].id == book2.id
        assert out_of_stock_books[0].stock == 0
