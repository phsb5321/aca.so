# tests/test_books.py
import pytest
from contextlib import asynccontextmanager
from app.database.gremlin import GraphDB
from app.database.models import BookCreate, BookUpdate, PersonCreate, RatingCreate
from app.services.books_services import BookUseCases, Book, Person, Rating


# Fixture to share an instance of BookUseCases between tests and clean up the connection after all tests are run
@asynccontextmanager
async def book_use_cases():
    graph_database = GraphDB()
    use_cases = BookUseCases(graph_database)
    try:
        yield use_cases
    finally:
        await graph_database.close_connection()


# Test the create_book method in BookUseCases
@pytest.mark.asyncio
async def test_create_book():
    async with book_use_cases() as use_cases:
        # Call the create_book method with a new BookCreate object
        created_book = await use_cases.create_book(BookCreate(title="Title", isbn="1234567890", stock=10, authors=["Author1", "Author2"]))

        # Check if the returned Book object has the correct id, title, isbn, stock, and authors
        assert isinstance(created_book.id, str)
        assert created_book.title == "Title"
        assert created_book.isbn == "1234567890"
        assert created_book.stock == 10
        assert len(created_book.authors) == 2
        assert isinstance(created_book.authors[0], Person)
        assert isinstance(created_book.authors[1], Person)


# Test the update_book method in BookUseCases
@pytest.mark.asyncio
async def test_update_book():
    async with book_use_cases() as use_cases:
        # Create a new book and update its title
        created_book = await use_cases.create_book(BookCreate(title="Title", isbn="1234567890", stock=10, authors=["Author1", "Author2"]))
        updated_book = await use_cases.update_book(created_book.id, BookUpdate(title="New Title"))

        # Check if the returned Book object has the correct id, updated title, isbn, stock, and authors
        assert updated_book.id == created_book.id
        assert updated_book.title == "New Title"
        assert updated_book.isbn == created_book.isbn
        assert updated_book.stock == created_book.stock
        assert len(updated_book.authors) == 2
        assert isinstance(updated_book.authors[0], Person)
        assert isinstance(updated_book.authors[1], Person)

# Test the delete_book method in BookUseCases


@pytest.mark.asyncio
async def test_delete_book():
    async with book_use_cases() as use_cases:
        # Create a new book and delete it
        created_book = await use_cases.create_book(BookCreate(title="Title", isbn="1234567890", stock=10, authors=["Author1", "Author2"]))
        await use_cases.delete_book(created_book.id)

        # Check if the book is actually deleted
        assert await use_cases.get_book(created_book.id) is None

# Test the get_book method in BookUseCases


@pytest.mark.asyncio
async def test_get_book():
    async with book_use_cases() as use_cases:
        # Create a new book and get it
        created_book = await use_cases.create_book(BookCreate(title="Title", isbn="1234567890", stock=10, authors=["Author1", "Author2"]))
        fetched_book = await use_cases.get_book(created_book.id)

        # Check if the fetched book has the same properties as the created one
        assert fetched_book.id == created_book.id
        assert fetched_book.title == created
