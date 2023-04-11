# usecases.py
from typing import List, Optional
from gremlin_python.process.graph_traversal import __

from database import GraphDB
from models import BookUpdate, PersonCreate, BookCreate, PersonUpdate, RatingCreate, Person, Book, Rating


db = GraphDB()
g = db.get_traversal()


def create_person(person: PersonCreate) -> Person:
    pass  # Implement create person logic


def update_person(person_id: int, person: PersonUpdate) -> Person:
    pass  # Implement update person logic


def delete_person(person_id: int) -> None:
    pass  # Implement delete person logic


def get_person(person_id: int) -> Optional[Person]:
    pass  # Implement get person logic


def get_persons(skip: int = 0, limit: int = 10) -> List[Person]:
    pass  # Implement get persons logic


def create_book(book: BookCreate) -> Book:
    pass  # Implement create book logic


def update_book(book_id: int, book: BookUpdate) -> Book:
    pass  # Implement update book logic


def delete_book(book_id: int) -> None:
    pass  # Implement delete book logic


def get_book(book_id: int) -> Optional[Book]:
    pass  # Implement get book logic


def get_books(skip: int = 0, limit: int = 10, in_stock: Optional[bool] = None) -> List[Book]:
    pass  # Implement get books logic


def get_books_by_author(author_id: int, skip: int = 0, limit: int = 10) -> List[Book]:
    pass  # Implement get books by author logic


def get_readers_by_book(book_id: int, skip: int = 0, limit: int = 10) -> List[Person]:
    pass  # Implement get readers by book logic


def get_ratings_by_book(book_id: int, skip: int = 0, limit: int = 10) -> List[Rating]:
    pass  # Implement get ratings by book logic


def create_rating(rating: RatingCreate) -> Rating:
    pass  # Implement create rating logic
