from typing import List, Optional
from app.database.gremlin import GraphDB
from app.database.models import BookUpdate, PersonCreate, BookCreate, PersonUpdate, RatingCreate, Person, Book, Rating
import uuid


class BookUseCases:
    def create_book(self, book: BookCreate) -> Book:
        pass  # Implement create book logic

    def update_book(self, book_id: int, book: BookUpdate) -> Book:
        pass  # Implement update book logic

    def delete_book(self, book_id: int) -> None:
        pass  # Implement delete book logic

    def get_book(self, book_id: int) -> Optional[Book]:
        pass  # Implement get book logic

    def get_books(self, skip: int = 0, limit: int = 10, in_stock: Optional[bool] = None) -> List[Book]:
        pass  # Implement get books logic

    def get_books_by_author(self, author_id: int, skip: int = 0, limit: int = 10) -> List[Book]:
        pass  # Implement get books by author logic

    def get_readers_by_book(self, book_id: int, skip: int = 0, limit: int = 10) -> List[Person]:
        pass  # Implement get readers by book logic

    def get_ratings_by_book(self, book_id: int, skip: int = 0, limit: int = 10) -> List[Rating]:
        pass  # Implement get ratings by book logic

    def create_rating(self, rating: RatingCreate) -> Rating:
        pass  # Implement create rating logic
